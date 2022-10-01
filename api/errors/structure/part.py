from api.errors.structure.base import BaseErrors


class PartErrors(BaseErrors):
    NOT_EXISTS = 'Part does not exist.'
    ALREADY_EXISTS = 'Part already exists.'
    SECTION_NOT_EXISTS = 'Section does not exist.'
