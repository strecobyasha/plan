from ..models.product import Product
from .base import BaseDataGenerator


class ProductsDataGenerator(BaseDataGenerator):
    table = 'products'
    fake_model = Product
