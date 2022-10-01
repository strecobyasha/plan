from api.models.associations import PartUnit, UnitAssociation
from api.models.models import Section


class Structure:

    @staticmethod
    def get_sections() -> dict:
        schedule = {}
        sections = Section.query.all()
        for section in sections:
            schedule[str(section.id)] = {'name': section.name, 'operations': {}, 'units': {}, 'parts': {}}

        return schedule

    @classmethod
    def get_units_and_parts(cls) -> dict:
        structure = cls.get_units()
        structure = cls.get_unit_parts(structure)
        structure = {x: y for x, y in sorted(structure.items(), key=lambda item: len(item[1]['parents']))}

        return structure

    @staticmethod
    def get_units() -> dict:
        # Structure of units.
        structure = {}
        for item in UnitAssociation.query.all():
            if str(item.unit_id) not in structure:
                structure[str(item.unit_id)] = {
                    'parents': [],
                    'children': [{'child_id': str(item.child_id), 'quantity': item.quantity}],
                    'parts': [],
                }
            else:
                structure[str(item.unit_id)]['children'].append({'child_id': str(item.child_id), 'quantity': item.quantity})

            if str(item.child_id) not in structure:
                structure[str(item.child_id)] = {
                    'parents': [str(item.unit_id)],
                    'children': [],
                    'parts': [],
                }
            else:
                structure[str(item.child_id)]['parents'].append(str(item.unit_id))

        return structure

    @staticmethod
    def get_unit_parts(structure: dict) -> dict:
        # Parts, that are included in units.
        for item in PartUnit.query.all():
            if str(item.unit_id) not in structure:
                structure[str(item.unit_id)] = {
                    'parents': [],
                    'children': [],
                    'parts': [{'part_id': str(item.part_id), 'quantity': item.quantity}],
                }
            else:
                structure[str(item.unit_id)]['parts'].append({'part_id': str(item.part_id), 'quantity': item.quantity})

        return structure
