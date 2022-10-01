from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from flask_pydantic_spec import Response

from api.app import spec
from api.containers.structure.section import ServiceContainer
from api.schema.structure.section import (CreateSectionBody,
                                          CreateSectionResponse,
                                          DeleteSectionParams,
                                          DeleteSectionResponse,
                                          GetSectionParams, GetSectionResponse,
                                          GetSectionsResponse,
                                          SectionOperationsParams,
                                          SectionOperationsResponse,
                                          SectionPartsBalanceResponse,
                                          SectionPartsParams,
                                          SectionPartsResponse,
                                          SectionUnitsBalanceResponse,
                                          SectionUnitsParams,
                                          SectionUnitsResponse,
                                          UpdateSectionBody,
                                          UpdateSectionParams,
                                          UpdateSectionResponse)
from api.services.structure.section import SectionService
from api.utils.decorators import json_response, unpack_models

bp = Blueprint('section', __name__)
TAG = 'Section'


@bp.route('/section/create', methods=['POST'])
@spec.validate(
    body=CreateSectionBody,
    resp=Response(HTTP_200=CreateSectionResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def create_section(
    body=CreateSectionBody,
    service: SectionService = Provide[ServiceContainer.service],
) -> CreateSectionResponse:
    """ Create the section.
        ---
    """
    section_id = service.create(name=body.name)

    return CreateSectionResponse(id=section_id, message=f'Section {body.name} is created.')


@bp.route('/section/get', methods=['GET'])
@spec.validate(
    query=GetSectionParams,
    resp=Response(HTTP_200=GetSectionResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def get_section(
    query=GetSectionParams,
    service: SectionService = Provide[ServiceContainer.service],
) -> GetSectionResponse:
    """ Get the section info.
        ---
    """
    section = service.get_item(id=query.id)

    return GetSectionResponse(
        id=query.id,
        name=section.name
    )


@bp.route('/sections/get', methods=['GET'])
@spec.validate(
    resp=Response(HTTP_200=GetSectionsResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def get_sections(
    service: SectionService = Provide[ServiceContainer.service],
) -> GetSectionsResponse:
    """ Get a list of sections.
        ---
    """

    return GetSectionsResponse(sections=service.get_list())


@bp.route('/section/update', methods=['PUT'])
@spec.validate(
    query=UpdateSectionParams,
    body=UpdateSectionBody,
    resp=Response(HTTP_200=UpdateSectionResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def update_section(
    query=UpdateSectionParams,
    body=UpdateSectionBody,
    service: SectionService = Provide[ServiceContainer.service],
) -> UpdateSectionResponse:
    """ Update the section.
        ---
    """
    section = service.update(id=query.id, name=body.name)

    return UpdateSectionResponse(id=query.id, name=section.name, message=f'Section {query.id} is updated.')


@bp.route('/section/delete', methods=['DELETE'])
@spec.validate(
    query=DeleteSectionParams,
    resp=Response(HTTP_200=DeleteSectionResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def delete_section(
    query=DeleteSectionParams,
    service: SectionService = Provide[ServiceContainer.service],
) -> DeleteSectionResponse:
    """ Delete the section.
        ---
    """
    service.delete(id=query.id)

    return DeleteSectionResponse(message=f'Section {query.id} is deleted.')


@bp.route('/section/parts', methods=['GET'])
@spec.validate(
    query=SectionPartsParams,
    resp=Response(HTTP_200=SectionPartsResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def get_parts(
    query=SectionPartsParams,
    service: SectionService = Provide[ServiceContainer.service],
) -> SectionPartsResponse:
    """ Get a list of section parts.
        ---
    """
    parts_list = service.get_parts(section_id=query.id)

    return SectionPartsResponse(parts=parts_list)


@bp.route('/section/parts/balance', methods=['GET'])
@spec.validate(
    query=SectionPartsParams,
    resp=Response(HTTP_200=SectionPartsBalanceResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def get_parts_balance(
    query=SectionPartsParams,
    service: SectionService = Provide[ServiceContainer.service],
) -> SectionPartsBalanceResponse:
    """ Get a list of section Parts with balance.
        ---
    """
    parts_list = service.get_parts_balance(section_id=query.id)

    return SectionPartsBalanceResponse(parts=parts_list)


@bp.route('/section/units', methods=['GET'])
@spec.validate(
    query=SectionUnitsParams,
    resp=Response(HTTP_200=SectionUnitsResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def get_units(
    query=SectionUnitsParams,
    service: SectionService = Provide[ServiceContainer.service],
) -> SectionUnitsResponse:
    """ Get a list of section units.
        ---
    """
    units_list = service.get_units(section_id=query.id)

    return SectionUnitsResponse(units=units_list)


@bp.route('/section/units/balance', methods=['GET'])
@spec.validate(
    query=SectionPartsParams,
    resp=Response(HTTP_200=SectionUnitsBalanceResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def get_units_balance(
    query=SectionPartsParams,
    service: SectionService = Provide[ServiceContainer.service],
) -> SectionUnitsBalanceResponse:
    """ Get a list of section units with balance.
        ---
    """
    parts_list = service.get_units_balance(section_id=query.id)

    return SectionUnitsBalanceResponse(units=parts_list)


@bp.route('/section/operations', methods=['GET'])
@spec.validate(
    query=SectionOperationsParams,
    resp=Response(HTTP_200=SectionOperationsResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def get_operations(
    query=SectionOperationsParams,
    service: SectionService = Provide[ServiceContainer.service],
) -> SectionOperationsResponse:
    """ Get a list of section operations.
        ---
    """
    operations_list = service.get_operations(section_id=query.id)

    return SectionOperationsResponse(operations=operations_list)
