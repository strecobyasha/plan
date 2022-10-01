from ..models.operation_product import OperationProduct
from .base import BaseDataGenerator


class OperationProductsDataGenerator(BaseDataGenerator):
    table = 'operation_products'
    fake_model = OperationProduct
