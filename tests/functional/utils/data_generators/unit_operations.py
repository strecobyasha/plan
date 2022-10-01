from ..models.unit_operation import UnitOperation
from .base import BaseDataGenerator


class UnitOperationsDataGenerator(BaseDataGenerator):
    table = 'unit_operations'
    fake_model = UnitOperation
