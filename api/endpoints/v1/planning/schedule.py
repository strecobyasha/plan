from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from flask_pydantic_spec import Response

from api.app import spec
from api.containers.planning.schedule import ServiceContainer
from api.schema.planning.schedule import CreateScheduleResponse
from api.services.planning.schedule import ScheduleService
from api.utils.decorators import json_response, unpack_models

bp = Blueprint('schedule', __name__)
TAG = 'Schedule'


@bp.route('/schedule/create', methods=['GET'])
@spec.validate(
    resp=Response(HTTP_200=CreateScheduleResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@inject
def create_schedule(
    service: ScheduleService = Provide[ServiceContainer.service],
) -> CreateScheduleResponse:
    """ Create the production schedule.
        ---
    """

    schedule = service.create_schedule()

    return CreateScheduleResponse(schedule=schedule)
