from http import HTTPStatus

import pytest

from ..utils.models.operation import Operation
from ..utils.models.part_operation import PartOperation
from ..utils.models.unit_operation import UnitOperation

pytestmark = pytest.mark.asyncio

test_operation = {}
FAKE_ID = '3fa85f64-5717-4562-b3fc-2c963f66afa6'


async def test_create_operation(make_request, generate_sections, generate_parts, generate_units):
    # Create operation.
    global test_operation
    test_operation = Operation(section_id=generate_sections[0]['id']).dict()
    test_operation['parts'] = [
        PartOperation(part_id=generate_parts[i]['id']).dict()
        for i in range(2)
    ]
    test_operation['units'] = [
        UnitOperation(unit_id=generate_units[i]['id']).dict()
        for i in range(2)
    ]

    response = await make_request(
        method='post',
        target='operation/create',
        json=test_operation,
    )

    test_operation['id'] = response.body.get('id')

    assert response.status == HTTPStatus.OK
    assert response.body.get('message') == f'Operation {test_operation["name"]} is created.'


async def test_create_existing_operation(make_request, generate_sections):
    # Create already existing operation.
    response = await make_request(
        method='post',
        target='operation/create',
        json=test_operation,
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('message') == f'Operation already exists.'


async def test_create_operation_not_full_data(make_request, generate_sections):
    # Create operation without a name.
    not_full_data = test_operation.copy()
    not_full_data.pop('name')
    response = await make_request(
        method='post',
        target='operation/create',
        json=not_full_data,
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_get_operation(make_request):
    # Get the operation.
    response = await make_request(
        method='get',
        target='operation/get',
        params={'id': test_operation['id']},
    )

    part_keys = ['part_id', 'quantity']
    unit_keys = ['unit_id', 'quantity']

    assert response.status == HTTPStatus.OK
    assert response.body['id'] == test_operation['id']
    assert response.body['name'] == test_operation['name']
    assert response.body['section_id'] == test_operation['section_id']

    assert [
               {key: element[key] for key in part_keys}
               for element in response.body['parts']
           ] == [
               {key: element[key] for key in part_keys}
               for element in test_operation['parts']
           ]

    assert [
               {key: element[key] for key in unit_keys}
               for element in response.body['units']
           ] == [
               {key: element[key] for key in unit_keys}
               for element in test_operation['units']
           ]


async def test_get_operation_not_exists(make_request):
    # Get not existing operation.
    response = await make_request(
        method='get',
        target='operation/get',
        params={'id': FAKE_ID},
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_get_operations(make_request):
    # Get list of operations.
    response = await make_request(
        method='get',
        target='operations/get',
    )
    operations = response.body.get('operations')

    assert response.status == HTTPStatus.OK
    assert test_operation['id'] in [element['id'] for element in operations]


async def test_update_operation(make_request):
    # Update operation.
    global test_operation
    operation_new_name = 'updated operation'
    test_operation['name'] = operation_new_name
    response = await make_request(
        method='put',
        target='operation/update',
        params={'id': test_operation['id']},
        json=test_operation,
    )

    assert response.status == HTTPStatus.OK
    assert response.body.get('name') == operation_new_name


async def test_update_operation_not_exists(make_request):
    # Update not existing operation.
    response = await make_request(
        method='put',
        target='operation/update',
        params={'id': FAKE_ID},
        json=test_operation,
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_delete_operation(make_request, pg_cursor):
    # Delete operation.
    response = await make_request(
        method='delete',
        target='operation/delete',
        params={'id': test_operation['id']},
    )

    assert response.status == HTTPStatus.OK
    assert response.body.get('message') == f"Operation {test_operation['id']} is deleted."


async def test_delete_operation_not_exists(make_request, pg_cursor):
    # Delete not existing operation.
    response = await make_request(
        method='delete',
        target='operation/delete',
        params={'id': FAKE_ID},
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
