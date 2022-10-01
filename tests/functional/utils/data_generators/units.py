from ..models.unit import Unit
from .base import BaseDataGenerator


class UnitsDataGenerator(BaseDataGenerator):
    table = 'units'
    fake_model = Unit
