from api.errors.structure.base import BaseErrors


class SectionErrors(BaseErrors):
    NOT_EXISTS = 'Section does not exist.'
    ALREADY_EXISTS = 'Section already exists.'
