from ..models.part_section import PartSection
from .base import BaseDataGenerator


class PartSectionsDataGenerator(BaseDataGenerator):
    table = 'part_sections'
    fake_model = PartSection
