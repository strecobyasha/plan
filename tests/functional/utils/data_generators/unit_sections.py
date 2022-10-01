from ..models.unit_section import UnitSection
from .base import BaseDataGenerator


class UnitSectionsDataGenerator(BaseDataGenerator):
    table = 'unit_sections'
    fake_model = UnitSection
