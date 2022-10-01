from http import HTTPStatus

import pytest

from ..utils.models.operation_product import OperationProduct
from ..utils.models.product import Product

pytestmark = pytest.mark.asyncio

test_product = {}
FAKE_ID = '3fa85f64-5717-4562-b3fc-2c963f66afa6'


async def test_create_product(make_request, generate_sections, generate_operations):
    # Create product.
    global test_product

    test_product = Product().dict()
    test_product['operations'] = [
        OperationProduct(operation_id=generate_operations[i]['id']).dict() for i in range(2)
    ]

    response = await make_request(
        method='post',
        target='product/create',
        json=test_product,
    )
    test_product['id'] = response.body.get('id')

    assert response.status == HTTPStatus.OK
    assert response.body.get('message') == f'Product {test_product["number"]} {test_product["name"]} ' \
                                           f'{test_product["customer"]} {test_product["contract"]} is created.'


async def test_create_existing_product(make_request):
    # Create already existing product.
    response = await make_request(
        method='post',
        target='product/create',
        json=test_product,
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('message') == f'Product already exists.'


async def test_create_product_not_full_data(make_request):
    # Create product without a name.
    not_full_data = test_product.copy()
    not_full_data.pop('name')
    response = await make_request(
        method='post',
        target='product/create',
        json=not_full_data,
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_get_product(make_request):
    # Get the product.
    response = await make_request(
        method='get',
        target='product/get',
        params={'id': test_product['id']},
    )
    assert response.status == HTTPStatus.OK
    assert response.body['id'] == test_product['id']
    assert response.body['name'] == test_product['name']
    assert response.body['contract'] == test_product['contract']
    assert response.body['customer'] == test_product['customer']
    assert [
               {'operation_id': element['operation_id']}
               for element in response.body['operations']
           ] == [
                {'operation_id': element['operation_id']}
               for element in test_product['operations']
           ]


async def test_get_product_not_exists(make_request):
    # Get not existing product.
    response = await make_request(
        method='get',
        target='product/get',
        params={'id': FAKE_ID},
    )
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_get_products(make_request):
    # Get list of products.
    response = await make_request(
        method='get',
        target='products/get',
    )
    products = response.body.get('products')

    assert response.status == HTTPStatus.OK
    assert test_product['id'] in [element['id'] for element in products]


async def test_update_product(make_request):
    # Update product.
    global test_product
    product_new_name = 'updated product'
    test_product['name'] = product_new_name
    response = await make_request(
        method='put',
        target='product/update',
        params={'id': test_product['id']},
        json=test_product,
    )

    assert response.status == HTTPStatus.OK
    assert response.body['name'] == product_new_name


async def test_update_product_not_exists(make_request):
    # Update not existing product.
    response = await make_request(
        method='put',
        target='product/update',
        params={'id': FAKE_ID},
        json=test_product,
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_delete_product(make_request, pg_cursor):
    # Delete product.
    response = await make_request(
        method='delete',
        target='product/delete',
        params={'id': test_product['id']},
    )

    assert response.status == HTTPStatus.OK
    assert response.body.get('message') == f"Product {test_product['id']} is deleted."


async def test_delete_product_not_exists(make_request, pg_cursor):
    # Delete not existing product.
    response = await make_request(
        method='delete',
        target='product/delete',
        params={'id': FAKE_ID},
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
