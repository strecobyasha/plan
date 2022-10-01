from ..models.part import Part
from .base import BaseDataGenerator


class PartsDataGenerator(BaseDataGenerator):
    table = 'parts'
    fake_model = Part
