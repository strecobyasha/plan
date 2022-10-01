import uuid
from http import HTTPStatus

from api.errors.structure.operation import OperationErrors
from api.maps.structure.operation import (OperationBriefMap, OperationFullMap,
                                          OperationGetPartMap,
                                          OperationGetUnitMap,
                                          OperationPartMap,
                                          OperationSetPartMap,
                                          OperationSetUnitMap,
                                          OperationUnitMap)
from api.models.associations import PartOperation, UnitOperation
from api.models.base import db
from api.models.models import Operation, Part, Unit
from api.services.structure.base import BaseService
from api.utils.system import json_abort


class OperationService(BaseService):
    error = OperationErrors
    model = Operation
    map = OperationBriefMap

    def get_item(self, id: uuid) -> OperationFullMap:
        operation = self.model.query.get(id)
        if not operation:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, self.error.NOT_EXISTS)

        return OperationFullMap(
            **operation.__dict__,
            **{
                'parts': [
                    OperationGetPartMap(
                        part_id=element.part_id,
                        number=element.part.number,
                        name=element.part.name,
                        quantity=element.quantity,
                    )
                    for element in operation.parts
                ],
                'units': [
                    OperationGetUnitMap(
                        unit_id=element.unit_id,
                        number=element.unit.number,
                        name=element.unit.name,
                        quantity=element.quantity,
                    )
                    for element in operation.units
                ],
            }
        )

    def add_parts(self, operation_id: uuid, parts: list[OperationSetPartMap]) -> None:
        # Add parts, that the operation contains.
        existing_operation_parts = {
            str(item.part_id): str(item.id)
            for item in PartOperation.query.filter_by(operation_id=operation_id)
        }
        for part in parts:
            map_data = OperationPartMap(**{'operation_id': operation_id, **part.dict()})
            if str(part.part_id) in existing_operation_parts:
                PartOperation.query.filter_by(
                    id=existing_operation_parts.pop(str(part.part_id)),
                ).update(map_data.dict())
                db.session.commit()
            elif not Part.query.get(part.part_id):
                json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, f'{part.part_id}: {self.error.PART_NOT_EXISTS}')
            else:
                element = PartOperation(**map_data.dict())
                element.insert_and_commit()

        delete_query = PartOperation.__table__.delete().where(
            PartOperation.id.in_(existing_operation_parts.values())
        )
        db.session.execute(delete_query)
        db.session.commit()

    def add_units(self, operation_id: uuid, units: list[OperationSetUnitMap]) -> None:
        # Add units, that the operation contains.
        existing_operation_units = {
            str(item.unit_id): str(item.id)
            for item in UnitOperation.query.filter_by(operation_id=operation_id)
        }
        for unit in units:
            map_data = OperationUnitMap(**{'operation_id': operation_id, **unit.dict()})
            if str(unit.unit_id) in existing_operation_units:
                UnitOperation.query.filter_by(
                    id=existing_operation_units.pop(str(unit.unit_id)),
                ).update(map_data.dict())
                db.session.commit()
            elif not Unit.query.get(unit.unit_id):
                json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, f'{unit.unit_id}: {self.error.UNIT_NOT_EXISTS}')
            else:
                element = UnitOperation(**map_data.dict())
                element.insert_and_commit()

        delete_query = UnitOperation.__table__.delete().where(
            UnitOperation.id.in_(existing_operation_units.values())
        )
        db.session.execute(delete_query)
        db.session.commit()
