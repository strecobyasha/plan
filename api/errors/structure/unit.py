from api.errors.structure.base import BaseErrors


class UnitErrors(BaseErrors):
    NOT_EXISTS = 'Unit does not exist.'
    ALREADY_EXISTS = 'Unit already exists.'
    SECTION_NOT_EXISTS = 'Section does not exist.'
    PART_NOT_EXISTS = 'Part does not exist.'
    UNIT_NOT_EXISTS = 'Unit does not exist.'
