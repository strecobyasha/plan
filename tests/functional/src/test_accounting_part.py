from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


FIRST_TRANSFER = 10
SECOND_TRANSFER = 8
THIRD_TRANSFER = 8
TRANSFER_DATE = '2022-09-23'


async def test_part_produced_first_point(
        make_request,
        generate_sections,
        generate_parts,
        generate_part_sections,
):
    # Add info about producing a part on its first point.
    test_part_id = generate_part_sections[0]['part_id']
    sender = generate_part_sections[0]['section_id']
    recipient = generate_part_sections[1]['section_id']

    response_add = await make_request(
        method='post',
        target='accounting/part',
        params={'id': test_part_id},
        json={
            "quantity": FIRST_TRANSFER,
            "sender_id": sender,
            "recipient_id": recipient,
            "transfer_date": TRANSFER_DATE
        }
    )

    response_get_sender_balance = await make_request(
        method='get',
        target='section/parts/balance',
        params={'id': sender},
    )

    response_get_recipient_balance = await make_request(
        method='get',
        target='section/parts/balance',
        params={'id': recipient},
    )

    assert response_add.status == HTTPStatus.OK

    for part in response_get_sender_balance.body['parts']:
        if part['id'] == test_part_id:
            assert part['balance'] == 0

    for part in response_get_recipient_balance.body['parts']:
        if part['id'] == test_part_id:
            assert part['balance'] == FIRST_TRANSFER + generate_part_sections[1]['balance']


async def test_part_produced_second_point(
        make_request,
        generate_sections,
        generate_parts,
        generate_part_sections,
):
    # Add info about producing a part on its second point.
    test_part_id = generate_part_sections[1]['part_id']
    sender = generate_part_sections[1]['section_id']
    recipient = generate_part_sections[2]['section_id']

    response_add = await make_request(
        method='post',
        target='accounting/part',
        params={'id': test_part_id},
        json={
            "quantity": SECOND_TRANSFER,
            "sender_id": sender,
            "recipient_id": recipient,
            "transfer_date": TRANSFER_DATE
        }
    )

    response_get_sender_balance = await make_request(
        method='get',
        target='section/parts/balance',
        params={'id': sender},
    )

    response_get_recipient_balance = await make_request(
        method='get',
        target='section/parts/balance',
        params={'id': recipient},
    )

    assert response_add.status == HTTPStatus.OK

    for part in response_get_sender_balance.body['parts']:
        if part['id'] == test_part_id:
            assert part['balance'] == FIRST_TRANSFER - SECOND_TRANSFER + generate_part_sections[1]['balance']

    for part in response_get_recipient_balance.body['parts']:
        if part['id'] == test_part_id:
            assert part['balance'] == SECOND_TRANSFER + generate_part_sections[2]['balance']


async def test_part_produced_second_point_excess(
        make_request,
        generate_sections,
        generate_parts,
        generate_part_sections,
):
    # Add info about producing a part on its second point with excess balance.
    test_part_id = generate_part_sections[1]['part_id']
    sender = generate_part_sections[1]['section_id']
    recipient = generate_part_sections[2]['section_id']

    response_add = await make_request(
        method='post',
        target='accounting/part',
        params={'id': test_part_id},
        json={
            "quantity": THIRD_TRANSFER,
            "sender_id": sender,
            "recipient_id": recipient,
            "transfer_date": TRANSFER_DATE
        }
    )

    response_get_sender_balance = await make_request(
        method='get',
        target='section/parts/balance',
        params={'id': sender},
    )

    response_get_recipient_balance = await make_request(
        method='get',
        target='section/parts/balance',
        params={'id': recipient},
    )

    assert response_add.status == HTTPStatus.OK

    for part in response_get_sender_balance.body['parts']:
        if part['id'] == test_part_id:
            assert part['balance'] == 0

    for part in response_get_recipient_balance.body['parts']:
        if part['id'] == test_part_id:
            assert part['balance'] == SECOND_TRANSFER + THIRD_TRANSFER + generate_part_sections[2]['balance']
