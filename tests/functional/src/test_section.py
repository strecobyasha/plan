from http import HTTPStatus

import pytest

from ..utils.models.section import Section

pytestmark = pytest.mark.asyncio

test_section = {}
FAKE_ID = '3fa85f64-5717-4562-b3fc-2c963f66afa6'


async def test_create_section(make_request):
    # Create section.
    global test_section
    test_section = Section().dict()
    response = await make_request(
        method='post',
        target='section/create',
        json=test_section,
    )
    test_section['id'] = response.body.get('id')

    assert response.status == HTTPStatus.OK
    assert response.body.get('message') == f'Section {test_section["name"]} is created.'


async def test_create_existing_section(make_request):
    # Create already existing section.
    response = await make_request(
        method='post',
        target='section/create',
        json=test_section,
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('message') == f'Section already exists.'


async def test_create_section_not_full_data(make_request):
    # Create a section without name.
    not_full_data = test_section.copy()
    not_full_data.pop('name')
    response = await make_request(
        method='post',
        target='unit/create',
        json=not_full_data,
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_get_section(make_request):
    # Get the section.
    response = await make_request(
        method='get',
        target='section/get',
        params={'id': test_section['id']},
    )

    assert response.status == HTTPStatus.OK
    assert response.body['id'] == test_section['id']
    assert response.body['name'] == test_section['name']


async def test_get_section_not_exists(make_request):
    # Get not existing section.
    response = await make_request(
        method='get',
        target='section/get',
        params={'id': FAKE_ID},
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_get_sections(make_request):
    # Get list of sections.
    response = await make_request(
        method='get',
        target='sections/get',
    )
    sections = response.body.get('sections')

    assert response.status == HTTPStatus.OK
    assert test_section['id'] in [element['id'] for element in sections]


async def test_update_section(make_request):
    # Update section.
    global test_section
    section_new_name = 'updated section'
    test_section['name'] = section_new_name
    response = await make_request(
        method='put',
        target='section/update',
        params={'id': test_section['id']},
        json=test_section,
    )

    assert response.status == HTTPStatus.OK
    assert response.body.get('name') == section_new_name


async def test_update_section_not_exists(make_request):
    # Update not existing section.
    response = await make_request(
        method='put',
        target='section/update',
        params={'id': FAKE_ID},
        json=test_section,
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_delete_section(make_request):
    # Delete section.
    response = await make_request(
        method='delete',
        target='section/delete',
        params={'id': test_section['id']},
    )

    assert response.status == HTTPStatus.OK
    assert response.body.get('message') == f"Section {test_section['id']} is deleted."


async def test_delete_section_not_exists(make_request):
    # Delete not existing section.
    response = await make_request(
        method='delete',
        target='section/delete',
        params={'id': FAKE_ID},
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_get_section_parts(
        make_request,
        generate_sections,
        generate_parts,
        generate_part_sections,
):
    # Get parts, that the section contains.
    test_object = generate_part_sections[0]

    response = await make_request(
        method='get',
        target='section/parts',
        params={'id': test_object['section_id']},
    )

    assert [
               {'id': response.body['parts'][0]['id'], 'cycle_time': response.body['parts'][0]['cycle_time']}
           ] == [{'id': test_object['part_id'], 'cycle_time': test_object['cycle_time']}]


async def test_get_section_parts_balance(
        make_request,
        generate_sections,
        generate_parts,
        generate_part_sections,
):
    # Get parts, that the section contains,with balance.
    test_object = generate_part_sections[0]

    response = await make_request(
        method='get',
        target='section/parts/balance',
        params={'id': test_object['section_id']},
    )

    assert [
               {'id': response.body['parts'][0]['id'], 'balance': response.body['parts'][0]['balance']}
           ] == [{'id': test_object['part_id'], 'balance': test_object['balance']}]


async def test_get_section_units(
        make_request,
        generate_sections,
        generate_units,
        generate_unit_sections,
):
    # Get units, that the section contains.
    test_object = generate_unit_sections[0]

    response = await make_request(
        method='get',
        target='section/units',
        params={'id': test_object['section_id']},
    )

    assert [
               {'id': response.body['units'][0]['id'], 'cycle_time': response.body['units'][0]['cycle_time']}
           ] == [{'id': test_object['unit_id'], 'cycle_time': test_object['cycle_time']}]


async def test_get_section_units_balance(
        make_request,
        generate_sections,
        generate_units,
        generate_unit_sections,
):
    # Get units, that the section contains,with balance.
    test_object = generate_unit_sections[0]

    response = await make_request(
        method='get',
        target='section/units/balance',
        params={'id': test_object['section_id']},
    )

    assert [
               {'id': response.body['units'][0]['id'], 'balance': response.body['units'][0]['balance']}
           ] == [{'id': test_object['unit_id'], 'balance': test_object['balance']}]
