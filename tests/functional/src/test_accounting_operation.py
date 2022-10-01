from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio

TRANSFER_DATE = '2022-09-23'


async def test_operation_complete(
        make_request,
        generate_sections,
        generate_parts,
        generate_units,
        generate_operations,
        generate_products,
        generate_part_sections,
        generate_unit_sections,
        generate_part_operations,
        generate_unit_operations,
        generate_operation_products,
):
    # Add info about completing an operation.
    operation_part = generate_part_operations[0]
    operation_unit = generate_unit_operations[1]
    test_operation = generate_operations[1]
    test_operation_product = generate_operation_products[1]

    response_add = await make_request(
        method='post',
        target='accounting/operation',
        params={'id': test_operation_product['operation_id']},
        json={
            "product_id": test_operation_product['product_id'],
            "completion_date": TRANSFER_DATE
        }
    )

    response_get_operation_balance = await make_request(
        method='get',
        target='product/get',
        params={'id': test_operation_product['product_id']},
    )

    response_get_sender_part_balance = await make_request(
        method='get',
        target='section/parts/balance',
        params={'id': test_operation['section_id']},
    )

    response_get_sender_unit_balance = await make_request(
        method='get',
        target='section/units/balance',
        params={'id': test_operation['section_id']},
    )

    assert response_add.status == HTTPStatus.OK

    for operation in response_get_operation_balance.body['operations']:
        if operation['operation_id'] == test_operation_product['operation_id']:
            assert operation['is_completed'] == True

    for part in response_get_sender_part_balance.body['parts']:
        if part['id'] == operation_part['part_id']:
            assert part['balance'] == generate_part_sections[6]['balance'] - operation_part['quantity']

    for unit in response_get_sender_unit_balance.body['units']:
        if unit['id'] == operation_unit['unit_id']:
            assert unit['balance'] == generate_unit_sections[6]['balance'] - operation_unit['quantity']


async def test_operation_complete_duplicate(
        make_request,
        generate_sections,
        generate_parts,
        generate_units,
        generate_operations,
        generate_products,
        generate_part_sections,
        generate_unit_sections,
        generate_part_operations,
        generate_unit_operations,
        generate_operation_products,
):
    # Add info about already completing an operation.
    operation_part = generate_part_operations[0]
    operation_unit = generate_unit_operations[1]
    test_operation = generate_operations[1]
    test_operation_product = generate_operation_products[1]

    response_add = await make_request(
        method='post',
        target='accounting/operation',
        params={'id': test_operation_product['operation_id']},
        json={
            "product_id": test_operation_product['product_id'],
            "completion_date": TRANSFER_DATE
        }
    )

    response_get_operation_balance = await make_request(
        method='get',
        target='product/get',
        params={'id': test_operation_product['product_id']},
    )

    response_get_sender_part_balance = await make_request(
        method='get',
        target='section/parts/balance',
        params={'id': test_operation['section_id']},
    )

    response_get_sender_unit_balance = await make_request(
        method='get',
        target='section/units/balance',
        params={'id': test_operation['section_id']},
    )

    assert response_add.status == HTTPStatus.UNPROCESSABLE_ENTITY

    for operation in response_get_operation_balance.body['operations']:
        if operation['operation_id'] == test_operation_product['operation_id']:
            assert operation['is_completed'] == True

    for part in response_get_sender_part_balance.body['parts']:
        if part['id'] == operation_part['part_id']:
            assert part['balance'] == generate_part_sections[6]['balance'] - operation_part['quantity']

    for unit in response_get_sender_unit_balance.body['units']:
        if unit['id'] == operation_unit['unit_id']:
            assert unit['balance'] == generate_unit_sections[6]['balance'] - operation_unit['quantity']
