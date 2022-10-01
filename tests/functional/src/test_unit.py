from http import HTTPStatus

import pytest

from ..utils.models.part_unit import PartUnit
from ..utils.models.unit import Unit
from ..utils.models.unit_section import UnitSection
from ..utils.models.unit_units import UnitUnits

pytestmark = pytest.mark.asyncio

test_unit = {}
FAKE_ID = '3fa85f64-5717-4562-b3fc-2c963f66afa6'


async def test_create_unit(make_request, generate_sections, generate_parts, generate_units):
    # Create unit.
    global test_unit

    test_unit = Unit().dict()
    test_unit['sections'] = [UnitSection(section_id=generate_sections[i]['id']).dict() for i in range(2)]
    test_unit['parts'] = [
        PartUnit(part_id=generate_parts[i]['id']).dict()
        for i in range(2)
    ]
    test_unit['units'] = [
        UnitUnits(child_id=generate_units[i]['id']).dict()
        for i in range(2)
    ]

    response = await make_request(
        method='post',
        target='unit/create',
        json=test_unit,
    )

    test_unit['id'] = response.body.get('id')

    assert response.status == HTTPStatus.OK
    assert response.body.get('message') == f'Unit {test_unit["number"]} {test_unit["name"]} is created.'


async def test_create_existing_unit(make_request):
    # Create already existing unit.
    response = await make_request(
        method='post',
        target='unit/create',
        json=test_unit,
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('message') == f'Unit already exists.'


async def test_create_unit_not_full_data(make_request):
    # Create a unit without name.
    not_full_data = test_unit.copy()
    not_full_data.pop('name')
    response = await make_request(
        method='post',
        target='unit/create',
        json=not_full_data,
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_get_unit(make_request):
    # Get the unit.
    response = await make_request(
        method='get',
        target='unit/get',
        params={'id': test_unit['id']},
    )

    section_keys = ['section_id', 'order_num', 'is_last_point', 'cycle_time', 'balance']
    part_keys = ['part_id', 'quantity']
    unit_keys = ['child_id', 'quantity']

    assert response.status == HTTPStatus.OK
    assert response.body['id'] == test_unit['id']
    assert len(response.body['sections']) == len(test_unit['sections'])

    assert [
               {key: element[key] for key in section_keys}
               for element in response.body['sections']
           ] == [
               {key: element[key] for key in section_keys}
               for element in test_unit['sections']
           ]

    assert [
               {key: element[key] for key in part_keys}
               for element in response.body['parts']
           ] == [
               {key: element[key] for key in part_keys}
               for element in test_unit['parts']
           ]

    assert [
               {key: element[key] for key in unit_keys}
               for element in response.body['unit_children']
           ] == [
               {key: element[key] for key in unit_keys}
               for element in test_unit['units']
           ]


async def test_get_unit_not_exists(make_request):
    # Get not existing unit.
    response = await make_request(
        method='get',
        target='unit/get',
        params={'id': FAKE_ID},
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_get_unit_parents(make_request, generate_units, generate_unit_units):
    # Get units containing the unit.
    test_object = generate_unit_units[0]

    response = await make_request(
        method='get',
        target='unit/get',
        params={'id': test_object['child_id']},
    )

    assert response.body['id'] == test_object['child_id']

    assert [
               {
                   'parent_id': response.body['unit_parents'][0]['parent_id'],
                   'quantity': response.body['unit_parents'][0]['quantity'],
               }
            ] == [
               {'parent_id': test_object['unit_id'], 'quantity': test_object['quantity']}
           ]


async def test_get_unit_operations(make_request, generate_units, generate_operations, generate_unit_operations):
    # Get operations containing the unit.
    test_object = generate_unit_operations[0]

    response = await make_request(
        method='get',
        target='unit/get',
        params={'id': test_object['unit_id']},
    )

    assert response.body['id'] == test_object['unit_id']
    assert response.body['operations'][0]['id'] == test_object['operation_id']
    assert response.body['operations'][0]['quantity'] == test_object['quantity']


async def test_get_units(make_request):
    # Get list of units.
    response = await make_request(
        method='get',
        target='units/get',
    )
    units = response.body.get('units')

    assert response.status == HTTPStatus.OK
    assert test_unit['id'] in [element['id'] for element in units]


async def test_update_unit(make_request, generate_sections):
    # Update unit.
    global test_unit
    unit_new_name = 'updated unit'
    test_unit['name'] = unit_new_name
    response = await make_request(
        method='put',
        target='unit/update',
        params={'id': test_unit['id']},
        json=test_unit,
    )

    assert response.status == HTTPStatus.OK
    assert response.body['name'] == unit_new_name


async def test_update_unit_not_exists(make_request, generate_sections):
    # Update not existing unit.
    response = await make_request(
        method='put',
        target='unit/update',
        params={'id': FAKE_ID},
        json=test_unit,
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_delete_unit(make_request, pg_cursor):
    # Delete unit.
    response = await make_request(
        method='delete',
        target='unit/delete',
        params={'id': test_unit['id']},
    )

    assert response.status == HTTPStatus.OK
    assert response.body.get('message') == f"Unit {test_unit['id']} is deleted."


async def test_delete_unit_not_exists(make_request, pg_cursor):
    # Delete not existing unit.
    response = await make_request(
        method='delete',
        target='unit/delete',
        params={'id': FAKE_ID},
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
