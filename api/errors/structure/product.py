from api.errors.structure.base import BaseErrors


class ProductErrors(BaseErrors):
    NOT_EXISTS = 'Product does not exist.'
    ALREADY_EXISTS = 'Product already exists.'
    OPERATION_NOT_EXISTS = 'Operation does not exist.'
