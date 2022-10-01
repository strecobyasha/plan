from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field

from api.maps.structure.product import (ProductBriefMap,
                                        ProductGetOperationMap,
                                        ProductSetOperationMap)


class CreateProductBody(BaseModel):
    number: str = Field(title='Product name')
    name: str = Field(title='Product name')
    customer: str = Field(title='Product customer')
    contract: str = Field(title='Number of contract')
    delivery_date: date = Field(title='Date of product delivery')
    operations: list[ProductSetOperationMap] = Field(title='Operations, that the product contains')


class CreateProductResponse(BaseModel):
    id: UUID = Field(title='Product id')
    message: str = Field(title='Response message')


class GetProductParams(BaseModel):
    id: UUID = Field(title='Product id')


class GetProductResponse(BaseModel):
    id: UUID = Field(title='Product id')
    number: str = Field(title='Product name')
    name: str = Field(title='Product name')
    customer: str = Field(title='Product customer')
    contract: str = Field(title='Number of contract')
    delivery_date: str = Field(title='Date of product delivery')
    operations: list[ProductGetOperationMap] = Field(title='Operations, which the product contains')


class GetProductsResponse(BaseModel):
    products: list[ProductBriefMap] = Field(title='List of products')


class UpdateProductParams(BaseModel):
    id: UUID = Field(title='Product id')


class UpdateProductBody(CreateProductBody):
    pass


class UpdateProductResponse(BaseModel):
    number: str = Field(title='Product name')
    name: str = Field(title='Product name')
    customer: str = Field(title='Product customer')
    contract: str = Field(title='Number of contract')
    delivery_date: str = Field(title='Date of product delivery')


class DeleteProductParams(BaseModel):
    id: UUID = Field(title='Product id')


class DeleteProductResponse(BaseModel):
    message: str = Field(title='Response message')
