from api.models.associations import PartSection, UnitSection


class Balance:

    @staticmethod
    def get_parts_balance_and_cycle() -> dict:
        parts = {}
        for item in PartSection.query.all():
            if str(item.part_id) not in parts:
                parts[str(item.part_id)] = []
            parts[str(item.part_id)].append(
                {
                    'section_id': str(item.section_id),
                    'order_num': item.order_num,
                    'is_last_point': item.is_last_point,
                    'cycle_time': item.cycle_time,
                    'balance': item.balance,
                }
            )

        return parts

    @staticmethod
    def get_units_balance_and_cycle():
        units = {}
        for item in UnitSection.query.all():
            if str(item.unit_id) not in units:
                units[str(item.unit_id)] = []
            units[str(item.unit_id)].append(
                {
                    'section_id': str(item.section_id),
                    'order_num': item.order_num,
                    'is_last_point': item.is_last_point,
                    'cycle_time': item.cycle_time,
                    'balance': item.balance,
                }
            )

        return units
