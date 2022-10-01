from ..models.part_operation import PartOperation
from .base import BaseDataGenerator


class PartOperationsDataGenerator(BaseDataGenerator):
    table = 'part_operations'
    fake_model = PartOperation
