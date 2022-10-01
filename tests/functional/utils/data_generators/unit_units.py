from ..models.unit_units import UnitUnits
from .base import BaseDataGenerator


class UnitUnitsDataGenerator(BaseDataGenerator):
    table = 'unit_association'
    fake_model = UnitUnits
