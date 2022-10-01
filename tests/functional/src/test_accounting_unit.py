from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio

FIRST_TRANSFER = 3
SECOND_TRANSFER = 2
THIRD_TRANSFER = 12
TRANSFER_DATE = '2022-09-23'


async def test_unit_produced_first_point(
        make_request,
        generate_sections,
        generate_parts,
        generate_units,
        generate_part_sections,
        generate_unit_sections,
        generate_part_units,
        generate_unit_units,
):
    # Add info about producing a unit on its first point.
    test_unit_id = generate_unit_sections[4]['unit_id']
    test_part_unit = generate_part_units[1]
    test_unit_unit = generate_unit_units[0]
    sender = generate_unit_sections[4]['section_id']
    recipient = generate_unit_sections[5]['section_id']

    response_add = await make_request(
        method='post',
        target='accounting/unit',
        params={'id': test_unit_id},
        json={
            "quantity": FIRST_TRANSFER,
            "sender_id": sender,
            "recipient_id": recipient,
            "transfer_date": TRANSFER_DATE
        }
    )

    response_get_sender_balance = await make_request(
        method='get',
        target='section/units/balance',
        params={'id': sender},
    )

    response_get_recipient_balance = await make_request(
        method='get',
        target='section/units/balance',
        params={'id': recipient},
    )

    response_get_sender_part_balance = await make_request(
        method='get',
        target='section/parts/balance',
        params={'id': sender},
    )

    response_get_sender_unit_balance = await make_request(
        method='get',
        target='section/units/balance',
        params={'id': sender},
    )

    assert response_add.status == HTTPStatus.OK

    for unit in response_get_sender_balance.body['units']:
        if unit['id'] == test_unit_id:
            assert unit['balance'] == 0

    for unit in response_get_recipient_balance.body['units']:
        if unit['id'] == test_unit_id:
            assert unit['balance'] == FIRST_TRANSFER + generate_unit_sections[5]['balance']

    for part in response_get_sender_part_balance.body['parts']:
        if part['id'] == test_part_unit['part_id']:
            assert part['balance'] == \
               generate_part_sections[2]['balance'] - FIRST_TRANSFER * test_part_unit['quantity']

    for unit in response_get_sender_unit_balance.body['units']:
        if unit['id'] == test_unit_unit['child_id']:
            assert unit['balance'] == \
               generate_unit_sections[1]['balance'] - FIRST_TRANSFER * test_unit_unit['quantity']


async def test_unit_produced_second_point(
        make_request,
        generate_sections,
        generate_parts,
        generate_units,
        generate_part_sections,
        generate_unit_sections,
        generate_part_units,
        generate_unit_units,
):
    # Add info about producing a unit on its second point.
    test_unit_id = generate_unit_sections[4]['unit_id']
    test_part_unit = generate_part_units[1]
    test_unit_unit = generate_unit_units[0]
    sender = generate_unit_sections[5]['section_id']
    recipient = generate_unit_sections[6]['section_id']

    response_add = await make_request(
        method='post',
        target='accounting/unit',
        params={'id': test_unit_id},
        json={
            "quantity": SECOND_TRANSFER,
            "sender_id": sender,
            "recipient_id": recipient,
            "transfer_date": TRANSFER_DATE
        }
    )

    response_get_sender_balance = await make_request(
        method='get',
        target='section/units/balance',
        params={'id': sender},
    )

    response_get_recipient_balance = await make_request(
        method='get',
        target='section/units/balance',
        params={'id': recipient},
    )

    response_get_sender_part_balance = await make_request(
        method='get',
        target='section/parts/balance',
        params={'id': generate_unit_sections[4]['section_id']},
    )

    response_get_sender_unit_balance = await make_request(
        method='get',
        target='section/units/balance',
        params={'id': generate_unit_sections[4]['section_id']},
    )

    assert response_add.status == HTTPStatus.OK

    for unit in response_get_sender_balance.body['units']:
        if unit['id'] == test_unit_id:
            assert unit['balance'] == FIRST_TRANSFER - SECOND_TRANSFER + generate_unit_sections[5]['balance']

    for unit in response_get_recipient_balance.body['units']:
        if unit['id'] == test_unit_id:
            assert unit['balance'] == SECOND_TRANSFER + generate_unit_sections[6]['balance']

    for part in response_get_sender_part_balance.body['parts']:
        if part['id'] == test_part_unit['part_id']:
            assert part['balance'] == \
               generate_part_sections[2]['balance'] - FIRST_TRANSFER * test_part_unit['quantity']

    for unit in response_get_sender_unit_balance.body['units']:
        if unit['id'] == test_unit_unit['child_id']:
            assert unit['balance'] == \
               generate_unit_sections[1]['balance'] - FIRST_TRANSFER * test_unit_unit['quantity']


async def test_unit_produced_second_point_excess(
        make_request,
        generate_sections,
        generate_parts,
        generate_units,
        generate_part_sections,
        generate_unit_sections,
        generate_part_units,
        generate_unit_units,
):
    # Add info about producing a unit on its second point with excess balance.
    test_unit_id = generate_unit_sections[4]['unit_id']
    test_part_unit = generate_part_units[1]
    test_unit_unit = generate_unit_units[0]
    sender = generate_unit_sections[5]['section_id']
    recipient = generate_unit_sections[6]['section_id']

    response_add = await make_request(
        method='post',
        target='accounting/unit',
        params={'id': test_unit_id},
        json={
            "quantity": THIRD_TRANSFER,
            "sender_id": sender,
            "recipient_id": recipient,
            "transfer_date": TRANSFER_DATE
        }
    )

    response_get_sender_balance = await make_request(
        method='get',
        target='section/units/balance',
        params={'id': sender},
    )

    response_get_recipient_balance = await make_request(
        method='get',
        target='section/units/balance',
        params={'id': recipient},
    )

    response_get_sender_part_balance = await make_request(
        method='get',
        target='section/parts/balance',
        params={'id': generate_unit_sections[4]['section_id']},
    )

    response_get_sender_unit_balance = await make_request(
        method='get',
        target='section/units/balance',
        params={'id': generate_unit_sections[4]['section_id']},
    )

    assert response_add.status == HTTPStatus.OK

    for unit in response_get_sender_balance.body['units']:
        if unit['id'] == test_unit_id:
            assert unit['balance'] == 0

    for unit in response_get_recipient_balance.body['units']:
        if unit['id'] == test_unit_id:
            assert unit['balance'] == SECOND_TRANSFER + THIRD_TRANSFER + generate_unit_sections[6]['balance']

    for part in response_get_sender_part_balance.body['parts']:
        if part['id'] == test_part_unit['part_id']:
            assert part['balance'] == \
               generate_part_sections[2]['balance'] - FIRST_TRANSFER * test_part_unit['quantity']

    for unit in response_get_sender_unit_balance.body['units']:
        if unit['id'] == test_unit_unit['child_id']:
            assert unit['balance'] == \
               generate_unit_sections[1]['balance'] - FIRST_TRANSFER * test_unit_unit['quantity']
