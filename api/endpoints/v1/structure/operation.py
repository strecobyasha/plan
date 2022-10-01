from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from flask_pydantic_spec import Response

from api.app import spec
from api.containers.structure.operation import ServiceContainer
from api.schema.structure.operation import (CreateOperationBody,
                                            CreateOperationResponse,
                                            DeleteOperationParams,
                                            DeleteOperationResponse,
                                            GetOperationParams,
                                            GetOperationResponse,
                                            GetOperationsResponse,
                                            UpdateOperationBody,
                                            UpdateOperationParams,
                                            UpdateOperationResponse)
from api.services.structure.operation import OperationService
from api.utils.decorators import json_response, unpack_models

bp = Blueprint('operation', __name__)
TAG = 'Operation'


@bp.route('/operation/create', methods=['POST'])
@spec.validate(
    body=CreateOperationBody,
    resp=Response(HTTP_200=CreateOperationResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def create_operation(
    body=CreateOperationBody,
    service: OperationService = Provide[ServiceContainer.service],
) -> CreateOperationResponse:
    """ Create the operation.
        ---
    """
    operation_id = service.create(
        name=body.name,
        cycle_time=body.cycle_time,
        advance=body.advance,
        section_id=body.section_id,
    )
    service.add_parts(operation_id=operation_id, parts=body.parts)
    service.add_units(operation_id=operation_id, units=body.units)

    return CreateOperationResponse(id=operation_id, message=f'Operation {body.name} is created.')


@bp.route('/operation/get', methods=['GET'])
@spec.validate(
    query=GetOperationParams,
    resp=Response(HTTP_200=GetOperationResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def get_operation(
    query=GetOperationParams,
    service: OperationService = Provide[ServiceContainer.service],
) -> GetOperationResponse:
    """ Get the operation info.
        ---
    """
    operation = service.get_item(id=query.id)

    return GetOperationResponse(**operation.__dict__)


@bp.route('/operations/get', methods=['GET'])
@spec.validate(
    resp=Response(HTTP_200=GetOperationsResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def get_operations(
    service: OperationService = Provide[ServiceContainer.service],
) -> GetOperationsResponse:
    """ Get a list of operations.
        ---
    """

    return GetOperationsResponse(operations=service.get_list())


@bp.route('/operation/update', methods=['PUT'])
@spec.validate(
    query=UpdateOperationParams,
    body=UpdateOperationBody,
    resp=Response(HTTP_200=UpdateOperationResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def update_operation(
    query=UpdateOperationParams,
    body=UpdateOperationBody,
    service: OperationService = Provide[ServiceContainer.service],
) -> UpdateOperationResponse:
    """ Update the operation.
        ---
    """
    operation = service.update(
        id=query.id,
        name=body.name,
        cycle_time=body.cycle_time,
        advance=body.advance,
        section_id=body.section_id,
    )
    service.add_parts(operation_id=query.id, parts=body.parts)
    service.add_units(operation_id=query.id, units=body.units)

    return UpdateOperationResponse(
        id=query.id,
        name=operation.name,
        cycle_time=operation.cycle_time,
        advance=operation.advance,
        section_id=operation.section_id,
        message=f'Operation {query.id} is updated.',
    )


@bp.route('/operation/delete', methods=['DELETE'])
@spec.validate(
    query=DeleteOperationParams,
    resp=Response(HTTP_200=DeleteOperationResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def delete_operation(
    query=DeleteOperationParams,
    service: OperationService = Provide[ServiceContainer.service],
) -> DeleteOperationResponse:
    """ Delete the operation.
        ---
    """
    service.delete(id=query.id)

    return DeleteOperationResponse(message=f'Operation {query.id} is deleted.')
