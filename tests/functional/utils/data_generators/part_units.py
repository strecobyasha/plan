from ..models.part_unit import PartUnit
from .base import BaseDataGenerator


class PartUnitsDataGenerator(BaseDataGenerator):
    table = 'part_units'
    fake_model = PartUnit
