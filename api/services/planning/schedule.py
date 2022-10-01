"""
The core service of the system.

1. Collect all sections.
2. Schedule operations by sections.
3. Schedule units, that are not children of any other units.
4. Schedule units, that are children of some other units.
5. Schedule parts.

"""

from copy import copy
from datetime import date, timedelta

from api.models.associations import OperationProduct

from .balance import Balance
from .structure import Structure

HORIZON = 60  # Scheduling horizon in days

class ScheduleService:

    def __init__(self):
        self.schedule = Structure.get_sections()
        self.structure = Structure.get_units_and_parts()
        self.parts = Balance.get_parts_balance_and_cycle()
        self.units = Balance.get_units_balance_and_cycle()

    def create_schedule(self) -> dict:
        self._schedule_operations()
        self._schedule_units()
        self._schedule_parts()

        return self.schedule

    def _schedule_operations(self) -> None:
        # STEP 1. Calculate how many units and parts do we need for all operations.
        operations = OperationProduct.query.filter_by(is_completed=False)
        for item in operations:
            operation_section = str(item.operation.section_id)
            delivery_date = item.product.delivery_date - timedelta(days=item.operation.advance)
            offset = (delivery_date-date.today()).days
            self.schedule[operation_section]['operations'][str(item.id)] = {
                'name': item.operation.name,
                'delivery_date': delivery_date,
            }
            for unit in item.operation.units:
                unit_id = str(unit.unit_id)
                quantity = unit.quantity
                if unit_id not in self.schedule[operation_section]['units']:
                    self.schedule[operation_section]['units'][unit_id] = [0] * HORIZON
                self.schedule[operation_section]['units'][unit_id][offset] += quantity

            for part in item.operation.parts:
                part_id = str(part.part_id)
                quantity = part.quantity
                if part_id not in self.schedule[operation_section]['parts']:
                    self.schedule[operation_section]['parts'][part_id] = [0] * HORIZON
                self.schedule[operation_section]['parts'][part_id][offset] += quantity

    def _schedule_units(self) -> None:
        # STEP 2. Take into account balances; calculate how many subunits and parts we need for units.
        while self.structure:
            # Looping through items, scheduling in a first place those without parents.
            for unit_id, details in self.structure.copy().items():
                if len(details['parents']):
                    continue
                # Sort unit sections from the last point to the first one.
                self.units[unit_id] = sorted(self.units[unit_id], key=lambda item: item['order_num'], reverse=True)
                current_schedule = [0] * HORIZON

                for section in self.units[unit_id]:
                    section_id = section['section_id']
                    cycle_time = section['cycle_time']
                    order_num = section['order_num']
                    balance = section['balance']

                    if section['is_last_point']:
                        demand = self._recalculate_schedule(
                            current_demand=self.schedule[section_id]['units'][unit_id],
                            balance=balance,
                        )
                        current_schedule = list(
                            x + y for x, y
                            in zip(demand, current_schedule)
                        )
                        del self.schedule[section_id]['units'][unit_id]
                    else:
                        self.schedule[section_id]['units'][unit_id] = [
                                                                        sum(current_schedule[:cycle_time+1])
                                                                      ] + current_schedule[cycle_time+1:] + [
                                                                        0] * cycle_time
                        # If this is a first point, we now have a ready schedule for the unit and can
                        # calculate demand for its subunits and parts.
                        if order_num == 1:
                            for child in details['children']:
                                child_id = child['child_id']
                                quantity = child['quantity']

                                if child_id not in self.schedule[section_id]['units']:
                                    self.schedule[section_id]['units'][child_id] = [0] * HORIZON

                                self.schedule[section_id]['units'][child_id] = list(
                                    x * quantity + y for x, y in
                                    zip(
                                        self.schedule[section_id]['units'][unit_id],
                                        self.schedule[section_id]['units'][child_id],
                                    )
                                )
                                self.structure[child_id]['parents'].remove(unit_id)

                            for part in details['parts']:
                                part_id = part['part_id']
                                quantity = part['quantity']

                                if part_id not in self.schedule[section_id]['parts']:
                                    self.schedule[section_id]['parts'][part_id] = [0] * HORIZON

                                self.schedule[section_id]['parts'][part_id] = list(
                                    x * quantity + y for x, y in
                                    zip(
                                        self.schedule[section_id]['units'][unit_id],
                                        self.schedule[section_id]['parts'][part_id],
                                    )
                                )
                        else:
                            current_schedule = self._recalculate_schedule(
                                current_demand=copy(self.schedule[section_id]['units'][unit_id]),
                                balance=balance,
                            )
                del self.structure[unit_id]

    def _schedule_parts(self) -> None:
        # STEP 3. Calculate schedule for parts.
        for part_id, details in self.parts.items():
            self.parts[part_id] = sorted(self.parts[part_id], key=lambda item: item['order_num'], reverse=True)
            current_schedule = [0] * HORIZON
            for section in self.parts[part_id]:
                section_id = section['section_id']
                cycle_time = section['cycle_time']
                order_num = section['order_num']
                balance = section['balance']

                if section['is_last_point']:
                    demand = self._recalculate_schedule(
                        current_demand=self.schedule[section_id]['parts'][part_id],
                        balance=balance,
                    )
                    current_schedule = list(
                        x + y for x, y
                        in zip(demand, current_schedule)
                    )
                    del self.schedule[section_id]['parts'][part_id]
                else:
                    self.schedule[section_id]['parts'][part_id] = [
                                                                      sum(current_schedule[:cycle_time + 1])
                                                                  ] + current_schedule[cycle_time + 1:] + [
                                                                      0] * cycle_time
                    if order_num > 1:
                        current_schedule = self._recalculate_schedule(
                            current_demand=copy(self.schedule[section_id]['parts'][part_id]),
                            balance=balance,
                        )

    def _recalculate_schedule(self, current_demand: list, balance: int) -> list:
        pointer = 0
        while balance > 0 and pointer < len(current_demand):
            current_pointer_demand = current_demand[pointer]
            current_demand[pointer] = max(current_pointer_demand - balance, 0)
            balance -= current_pointer_demand
            pointer += 1

        return current_demand
