import uuid
from datetime import date

from pydantic import BaseModel, Field

from api.maps.base import get_new_id


class ProductSetOperationMap(BaseModel):
    operation_id: uuid.UUID = Field(title='Operation id', default_factory=get_new_id)
    is_completed: bool = Field(title='The operation is completed or not', default=False)


class ProductGetOperationMap(ProductSetOperationMap):
    name: str = Field(title='Operation name')
    cycle_time: int = Field(title='Operation production cycle')
    advance: int = Field(title='Operation advance time relative to the product target time')


class ProductOperationMap(ProductSetOperationMap):
    id: uuid.UUID = Field(title='OperationProduct id', default_factory=get_new_id)
    product_id: uuid.UUID = Field(title='Product id')


class ProductBriefMap(BaseModel):
    id: uuid.UUID = Field(title='Product id', default_factory=get_new_id)
    number: str = Field(title='Product name')
    name: str = Field(title='Product name')
    customer: str = Field(title='Product customer')
    contract: str = Field(title='Number of contract')
    delivery_date: date = Field(title='Date of product delivery')


class ProductFullMap(ProductBriefMap):
    operations: list = Field(title='Operations, that the product contains')
