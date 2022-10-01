from ..models.operation import Operation
from .base import BaseDataGenerator


class OperationsDataGenerator(BaseDataGenerator):
    table = 'operations'
    fake_model = Operation
