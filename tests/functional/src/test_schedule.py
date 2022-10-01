import json

import pytest

pytestmark = pytest.mark.asyncio

async def test_operation_complete(
        make_request,
        generate_sections,
        generate_parts,
        generate_units,
        generate_operations,
        generate_part_sections,
        generate_unit_sections,
        generate_products,
        generate_part_units,
        generate_unit_units,
        generate_part_operations,
        generate_unit_operations,
        generate_operation_products,
):
    response = await make_request(
        method='get',
        target='schedule/create',
    )

    with open('functional/test_data/expected_schedule.json') as file:
        expected = json.load(file)

    assert expected == response.body
