from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from flask_pydantic_spec import Response

from api.app import spec
from api.containers.structure.product import ServiceContainer
from api.schema.structure.product import (CreateProductBody,
                                          CreateProductResponse,
                                          DeleteProductParams,
                                          DeleteProductResponse,
                                          GetProductParams, GetProductResponse,
                                          GetProductsResponse,
                                          UpdateProductBody,
                                          UpdateProductParams,
                                          UpdateProductResponse)
from api.services.structure.product import ProductService
from api.utils.decorators import json_response, unpack_models

bp = Blueprint('product', __name__)
TAG = 'Product'


@bp.route('/product/create', methods=['POST'])
@spec.validate(
    body=CreateProductBody,
    resp=Response(HTTP_200=CreateProductResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def create_product(
    body=CreateProductBody,
    service: ProductService = Provide[ServiceContainer.service],
) -> CreateProductResponse:
    """ Create the product.
        ---
    """
    product_id = service.create(
        number=body.number,
        name=body.name,
        customer=body.customer,
        contract=body.contract,
        delivery_date=body.delivery_date,
    )
    service.add_operations(product_id=product_id, operations=body.operations)

    return CreateProductResponse(
        id=product_id,
        message=f'Product {body.number} {body.name} {body.customer} {body.contract} is created.',
    )


@bp.route('/product/get', methods=['GET'])
@spec.validate(
    query=GetProductParams,
    resp=Response(HTTP_200=GetProductResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def get_product(
    query=GetProductParams,
    service: ProductService = Provide[ServiceContainer.service],
) -> GetProductResponse:
    """ Get the product info.
        ---
    """
    product = service.get_item(id=query.id)
    product_dict = product.__dict__
    product_dict['delivery_date'] = product_dict['delivery_date'].strftime('%Y-%m-%d')

    return GetProductResponse(**product_dict)


@bp.route('/products/get', methods=['GET'])
@spec.validate(
    resp=Response(HTTP_200=GetProductsResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def get_products(
    service: ProductService = Provide[ServiceContainer.service],
) -> GetProductsResponse:
    """ Get a list of products.
        ---
    """
    products = service.get_list()
    for product in products:
        product.__dict__['delivery_date'] = product.__dict__['delivery_date'].strftime('%Y-%m-%d')

    return GetProductsResponse(products=products)


@bp.route('/product/update', methods=['PUT'])
@spec.validate(
    query=UpdateProductParams,
    body=UpdateProductBody,
    resp=Response(HTTP_200=UpdateProductResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def update_product(
    query=UpdateProductParams,
    body=UpdateProductBody,
    service: ProductService = Provide[ServiceContainer.service],
) -> UpdateProductResponse:
    """ Update the product.
        ---
    """
    product = service.update(
        id=query.id,
        number=body.number,
        name=body.name,
        customer=body.customer,
        contract=body.contract,
        delivery_date=body.delivery_date,
    )
    service.add_operations(product_id=query.id, operations=body.operations)

    return UpdateProductResponse(
        id=query.id,
        number=product.number,
        name=product.name,
        customer=product.customer,
        contract=product.contract,
        delivery_date=body.delivery_date.strftime('%Y-%m-%d'),
        message=f'Product {query.id} is updated.',
    )


@bp.route('/product/delete', methods=['DELETE'])
@spec.validate(
    query=DeleteProductParams,
    resp=Response(HTTP_200=DeleteProductResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def delete_product(
    query=DeleteProductParams,
    service: ProductService = Provide[ServiceContainer.service],
) -> DeleteProductResponse:
    """ Delete the product.
        ---
    """
    service.delete(id=query.id)

    return DeleteProductResponse(message=f'Product {query.id} is deleted.')
