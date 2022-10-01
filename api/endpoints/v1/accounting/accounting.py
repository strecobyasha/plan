from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from flask_pydantic_spec import Response

from api.app import spec
from api.containers.accounting.accounting import ServiceContainer
from api.schema.accounting.accounting import (CompletingOperationBody,
                                              CompletingOperationParams,
                                              CompletingOperationResponse,
                                              TransferItemBody,
                                              TransferItemParams,
                                              TransferItemResponse)
from api.services.accounting.operations import OperationsAccountingService
from api.services.accounting.parts import PartsAccountingService
from api.services.accounting.units import UnitsAccountingService
from api.utils.decorators import json_response, unpack_models

bp = Blueprint('accounting', __name__)
TAG = 'Accounting'


@bp.route('/accounting/part', methods=['POST'])
@spec.validate(
    body=TransferItemBody,
    query=TransferItemParams,
    resp=Response(HTTP_200=TransferItemResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def part_transfer(
    body=TransferItemBody,
    query=TransferItemParams,
    service: PartsAccountingService = Provide[ServiceContainer.parts_acc_service],
) -> TransferItemResponse:
    """ Accounting for the transfer of parts.
        ---
    """
    service.record(
        item_id=query.id,
        transfer_date=body.transfer_date,
        sender_id=body.sender_id,
        recipient_id=body.recipient_id,
        quantity=body.quantity,
    )
    service.change_balance(
        part_id=query.id,
        section_id=body.sender_id,
        quantity=body.quantity,
        role='sender',
    )
    service.change_balance(
        part_id=query.id,
        section_id=body.recipient_id,
        quantity=body.quantity,
        role='recipient',
    )

    return TransferItemResponse(message=f'Transfer data for the part {query.id} is recorded')


@bp.route('/accounting/unit', methods=['POST'])
@spec.validate(
    body=TransferItemBody,
    query=TransferItemParams,
    resp=Response(HTTP_200=TransferItemResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def unit_transfer(
    body=TransferItemBody,
    query=TransferItemParams,
    units_acc_service: UnitsAccountingService = Provide[ServiceContainer.units_acc_service],
    parts_acc_service: PartsAccountingService = Provide[ServiceContainer.parts_acc_service],
) -> TransferItemResponse:
    """ Accounting for the transfer of units.
        ---
    """
    units_acc_service.record(
        item_id=query.id,
        transfer_date=body.transfer_date,
        sender_id=body.sender_id,
        recipient_id=body.recipient_id,
        quantity=body.quantity,
    )
    units_acc_service.change_balance(
        unit_id=query.id,
        section_id=body.recipient_id,
        quantity=body.quantity,
        role='recipient',
    )
    unit_parts = units_acc_service.change_balance(
        unit_id=query.id,
        section_id=body.sender_id,
        quantity=body.quantity,
        role='sender',
    )
    for part in unit_parts:
        parts_acc_service.change_balance(
            part_id=part.part_id,
            section_id=body.sender_id,
            quantity=body.quantity * part.quantity,
            role='sender',
        )

    return TransferItemResponse(message=f'Transfer data for the unit {query.id} is recorded')


@bp.route('/accounting/operation', methods=['POST'])
@spec.validate(
    body=CompletingOperationBody,
    query=CompletingOperationParams,
    resp=Response(HTTP_200=CompletingOperationResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def operation_completing(
    body=CompletingOperationBody,
    query=CompletingOperationParams,
    units_acc_service: UnitsAccountingService = Provide[ServiceContainer.units_acc_service],
    parts_acc_service: PartsAccountingService = Provide[ServiceContainer.parts_acc_service],
    operations_acc_service: OperationsAccountingService = Provide[ServiceContainer.operations_acc_service],
) -> CompletingOperationResponse:
    """ Accounting for the completing of operations.
        ---
    """
    operations_acc_service.record(
        operation_id=query.id,
        product_id=body.product_id,
        completion_date=body.completion_date,
    )
    components = operations_acc_service.change_balance(
        operation_id=query.id,
        product_id=body.product_id,
    )
    for part in components['parts']:
        parts_acc_service.change_balance(
            part_id=part.part_id,
            section_id=components['section_id'],
            quantity=-part.quantity,
            role='producer',
        )
    for unit in components['units']:
        units_acc_service.change_balance(
            unit_id=unit.unit_id,
            section_id=components['section_id'],
            quantity=-unit.quantity,
            role='producer',
        )

    return CompletingOperationResponse(message=f'Data about completing of the operation {query.id} is recorded')
