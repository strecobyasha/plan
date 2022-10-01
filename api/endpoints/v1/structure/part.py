from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from flask_pydantic_spec import Response

from api.app import spec
from api.containers.structure.part import ServiceContainer
from api.schema.structure.part import (CreatePartBody, CreatePartResponse,
                                       DeletePartParams, DeletePartResponse,
                                       GetPartParams, GetPartResponse,
                                       GetPartsResponse, UpdatePartBody,
                                       UpdatePartParams, UpdatePartResponse)
from api.services.structure.part import PartService
from api.utils.decorators import json_response, unpack_models

bp = Blueprint('part', __name__)
TAG = 'Part'


@bp.route('/part/create', methods=['POST'])
@spec.validate(
    body=CreatePartBody,
    resp=Response(HTTP_200=CreatePartResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def create_part(
    body=CreatePartBody,
    service: PartService = Provide[ServiceContainer.service],
) -> CreatePartResponse:
    """ Create the part.
        ---
    """
    part_id = service.create(number=body.number, name=body.name)
    service.add_sections(part_id=part_id, sections=body.sections)

    return CreatePartResponse(id=part_id, message=f'Part {body.number} {body.name} is created.')


@bp.route('/part/get', methods=['GET'])
@spec.validate(
    query=GetPartParams,
    resp=Response(HTTP_200=GetPartResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def get_part(
    query=GetPartParams,
    service: PartService = Provide[ServiceContainer.service],
) -> GetPartResponse:
    """ Get the part info.
        ---
    """
    part = service.get_item(id=query.id)

    return GetPartResponse(**part.__dict__)


@bp.route('/parts/get', methods=['GET'])
@spec.validate(
    resp=Response(HTTP_200=GetPartsResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def get_parts(
    service: PartService = Provide[ServiceContainer.service],
) -> GetPartsResponse:
    """ Get a list of parts.
        ---
    """

    return GetPartsResponse(parts=service.get_list())


@bp.route('/part/update', methods=['PUT'])
@spec.validate(
    body=UpdatePartBody,
    query=UpdatePartParams,
    resp=Response(HTTP_200=UpdatePartResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def update_part(
    body=UpdatePartBody,
    query=UpdatePartParams,
    service: PartService = Provide[ServiceContainer.service],
) -> UpdatePartResponse:
    """ Update the part.
        ---
    """
    part = service.update(id=query.id, number=body.number, name=body.name)
    service.add_sections(part_id=query.id, sections=body.sections)

    return UpdatePartResponse(
        id=query.id,
        number=part.number,
        name=part.name,
        message=f'Part {query.id} is updated.',
    )


@bp.route('/part/delete', methods=['DELETE'])
@spec.validate(
    query=DeletePartParams,
    resp=Response(HTTP_200=DeletePartResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def delete_part(
    query=DeletePartParams,
    service: PartService = Provide[ServiceContainer.service],
) -> DeletePartResponse:
    """ Delete the part.
        ---
    """
    service.delete(id=query.id)

    return DeletePartResponse(message=f'Part {query.id} is deleted.')
