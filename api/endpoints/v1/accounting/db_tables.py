from flask import Blueprint
from flask_pydantic_spec import Response

from api.app import spec
from api.models.accounting_models import BaseAccountingModel
from api.schema.accounting.db_tables import (CreateTablesBodyParams,
                                             CreateTablesResponse)
from api.utils.decorators import json_response, unpack_models

bp = Blueprint('db_tables', __name__)
TAG = 'Tables'


@bp.route('/db_tables/create', methods=['POST'])
@spec.validate(
    body=CreateTablesBodyParams,
    resp=Response(HTTP_200=CreateTablesResponse),
    tags=[TAG],
)
@unpack_models
@json_response
def create_table(body: CreateTablesBodyParams):
    """ Create partition
    ---
    """

    target_date = body.target_date

    BaseAccountingModel.create_partition(target_date, 'parts_transfer_history')
    BaseAccountingModel.create_partition(target_date, 'units_transfer_history')
    BaseAccountingModel.create_partition(target_date, 'operations_history')

    return CreateTablesResponse(message='Tables are created.')
