from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from flask_pydantic_spec import Response

from api.app import spec
from api.containers.structure.unit import ServiceContainer
from api.schema.structure.unit import (CreateUnitBody, CreateUnitResponse,
                                       DeleteUnitParams, DeleteUnitResponse,
                                       GetUnitParams, GetUnitResponse,
                                       GetUnitsResponse, UpdateUnitBody,
                                       UpdateUnitParams, UpdateUnitResponse)
from api.services.structure.unit import UnitService
from api.utils.decorators import json_response, unpack_models

bp = Blueprint('unit', __name__)
TAG = 'Unit'


@bp.route('/unit/create', methods=['POST'])
@spec.validate(
    body=CreateUnitBody,
    resp=Response(HTTP_200=CreateUnitResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def create_unit(
    body=CreateUnitBody,
    service: UnitService = Provide[ServiceContainer.service],
) -> CreateUnitResponse:
    
    """ Create the unit.
        ---
    """
    unit_id = service.create(number=body.number, name=body.name)
    service.add_sections(unit_id=unit_id, sections=body.sections)
    service.add_parts(unit_id=unit_id, parts=body.parts)
    service.add_units(unit_id=unit_id, units=body.units)

    return CreateUnitResponse(id=unit_id, message=f'Unit {body.number} {body.name} is created.')


@bp.route('/unit/get', methods=['GET'])
@spec.validate(
    query=GetUnitParams,
    resp=Response(HTTP_200=GetUnitResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def get_unit(
    query=GetUnitParams,
    service: UnitService = Provide[ServiceContainer.service],
) -> GetUnitResponse:
    """ Get the unit info.
        ---
    """
    unit = service.get_item(id=query.id)

    return GetUnitResponse(**unit.__dict__)


@bp.route('/units/get', methods=['GET'])
@spec.validate(
    resp=Response(HTTP_200=GetUnitsResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def get_units(
    service: UnitService = Provide[ServiceContainer.service],
) -> GetUnitsResponse:
    """ Get a list of units.
        ---
    """

    return GetUnitsResponse(units=service.get_list())


@bp.route('/unit/update', methods=['PUT'])
@spec.validate(
    query=UpdateUnitParams,
    body=UpdateUnitBody,
    resp=Response(HTTP_200=UpdateUnitResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def update_unit(
    query=UpdateUnitParams,
    body=UpdateUnitBody,
    service: UnitService = Provide[ServiceContainer.service],
) -> UpdateUnitResponse:
    """ Update the unit.
        ---
    """
    unit = service.update(id=query.id, number=body.number, name=body.name)
    service.add_sections(unit_id=query.id, sections=body.sections)
    service.add_parts(unit_id=query.id, parts=body.parts)
    service.add_units(unit_id=query.id, units=body.units)

    return UpdateUnitResponse(
        id=query.id,
        number=unit.number,
        name=unit.name,
        message=f'Unit {query.id} is updated.',
    )


@bp.route('/unit/delete', methods=['DELETE'])
@spec.validate(
    query=DeleteUnitParams,
    resp=Response(HTTP_200=DeleteUnitResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def delete_unit(
    query=DeleteUnitParams,
    service: UnitService = Provide[ServiceContainer.service],
) -> DeleteUnitResponse:
    """ Delete the unit.
        ---
    """
    service.delete(id=query.id)

    return DeleteUnitResponse(message=f'Unit {query.id} is deleted.')
