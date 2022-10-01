from http import HTTPStatus

import pytest

from ..utils.models.part import Part
from ..utils.models.part_section import PartSection

pytestmark = pytest.mark.asyncio

test_part = {}
FAKE_ID = '3fa85f64-5717-4562-b3fc-2c963f66afa6'


async def test_create_part(make_request, generate_sections):
    # Create part.
    global test_part

    test_part = Part().dict()
    test_part['sections'] = [PartSection(section_id=generate_sections[i]['id']).dict() for i in range(2)]

    response = await make_request(
        method='post',
        target='part/create',
        json=test_part,
    )

    test_part['id'] = response.body.get('id')

    assert response.status == HTTPStatus.OK
    assert response.body.get('message') == f'Part {test_part["number"]} {test_part["name"]} is created.'


async def test_create_existing_part(make_request):
    # Create already existing part.
    response = await make_request(
        method='post',
        target='part/create',
        json=test_part,
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('message') == f'Part already exists.'


async def test_create_part_not_full_data(make_request):
    # Create a part without name.
    not_full_data = test_part.copy()
    not_full_data.pop('name')
    response = await make_request(
        method='post',
        target='part/create',
        json=not_full_data,
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_get_part(make_request):
    # Get the part.
    response = await make_request(
        method='get',
        target='part/get',
        params={'id': test_part['id']},
    )

    section_keys = ['section_id', 'order_num', 'is_last_point', 'cycle_time', 'balance']

    assert response.status == HTTPStatus.OK
    assert response.body['id'] == test_part['id']

    assert [
               {key: element[key] for key in section_keys}
               for element in response.body['sections']
            ] == [
                {key: element[key] for key in section_keys}
                for element in test_part['sections']
            ]


async def test_get_part_not_exists(make_request):
    # Get not existing part.
    response = await make_request(
        method='get',
        target='part/get',
        params={'id': FAKE_ID},
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_get_part_units(make_request, generate_parts, generate_units, generate_part_units):
    # Get units containing the part.
    test_object = generate_part_units[0]

    response = await make_request(
        method='get',
        target='part/get',
        params={'id': test_object['part_id']},
    )

    assert response.body['id'] == test_object['part_id']
    assert response.body['units'][0]['id'] == test_object['unit_id']
    assert response.body['units'][0]['quantity'] == test_object['quantity']


async def test_get_part_operations(make_request, generate_parts, generate_operations, generate_part_operations):
    # Get operations containing the part.
    test_object = generate_part_operations[0]

    response = await make_request(
        method='get',
        target='part/get',
        params={'id': test_object['part_id']},
    )

    assert response.body['id'] == test_object['part_id']
    assert response.body['operations'][0]['id'] == test_object['operation_id']
    assert response.body['operations'][0]['quantity'] == test_object['quantity']


async def test_get_parts(make_request):
    # Get list of parts.
    response = await make_request(
        method='get',
        target='parts/get',
    )
    parts = response.body.get('parts')

    assert response.status == HTTPStatus.OK
    assert test_part['id'] in [element['id'] for element in parts]


async def test_update_part(make_request):
    # Update part.
    global test_part
    part_new_name = 'updated part'
    test_part['name'] = part_new_name

    response = await make_request(
        method='put',
        target='part/update',
        params={'id': test_part['id']},
        json=test_part,
    )

    assert response.status == HTTPStatus.OK
    assert response.body['name'] == part_new_name


async def test_update_part_not_exists(make_request):
    # Update not existing part.
    response = await make_request(
        method='put',
        target='part/update',
        params={'id': FAKE_ID},
        json=test_part,
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_delete_part(make_request, pg_cursor):
    # Delete part.
    response = await make_request(
        method='delete',
        target='part/delete',
        params={'id': test_part['id']},
    )

    assert response.status == HTTPStatus.OK
    assert response.body.get('message') == f"Part {test_part['id']} is deleted."


async def test_delete_part_not_exists(make_request, pg_cursor):
    # Delete not existing part.
    response = await make_request(
        method='delete',
        target='part/delete',
        params={'id': FAKE_ID},
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
