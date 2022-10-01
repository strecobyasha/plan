from ..models.section import Section
from .base import BaseDataGenerator


class SectionsDataGenerator(BaseDataGenerator):
    table = 'sections'
    fake_model = Section
