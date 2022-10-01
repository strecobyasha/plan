import uuid
from http import HTTPStatus

from api.errors.structure.part import PartErrors
from api.maps.structure.part import (PartBriefMap, PartFullMap,
                                     PartGetSectionMap, PartOperationMap,
                                     PartSectionMap, PartSetSectionMap,
                                     PartUnitMap)
from api.models.associations import PartSection
from api.models.base import db
from api.models.models import Part, Section
from api.services.structure.base import BaseService
from api.utils.system import json_abort


class PartService(BaseService):
    error = PartErrors
    model = Part
    map = PartBriefMap

    def get_item(self, id: uuid) -> PartFullMap:
        part = self.model.query.get(id)
        if not part:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, self.error.NOT_EXISTS)

        return PartFullMap(
            **part.__dict__,
            **{
                'units': [
                    PartUnitMap(
                        id=element.unit_id,
                        number=element.unit.number,
                        name=element.unit.name,
                        quantity=element.quantity,
                    )
                    for element in part.units
                ],
                'operations': [
                    PartOperationMap(
                        id=element.operation_id,
                        name=element.operation.name,
                        quantity=element.quantity,
                    )
                    for element in part.operations
                ],
                'sections': [
                    PartGetSectionMap(
                        section_id=element.section_id,
                        section_name=element.section.name,
                        order_num=element.order_num,
                        is_last_point=element.is_last_point,
                        cycle_time=element.cycle_time,
                        balance=element.balance,
                    )
                    for element in part.sections
                ]
            }
        )

    def add_sections(self, part_id: uuid, sections: list[PartSetSectionMap]) -> None:
        # Set a route of the part through the sections.
        existing_part_sections = {
            str(item.section_id): str(item.id)
            for item in PartSection.query.filter_by(part_id=part_id)
        }
        for section in sections:
            map_data = PartSectionMap(**{'part_id': part_id, **section.dict()})
            if str(section.section_id) in existing_part_sections:
                PartSection.query.filter_by(
                    id=existing_part_sections.pop(str(section.section_id)),
                ).update(map_data.dict())
                db.session.commit()
            elif not Section.query.get(section.section_id):
                json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, f'{section.section_id}: {self.error.SECTION_NOT_EXISTS}')
            else:
                element = PartSection(**map_data.dict())
                element.insert_and_commit()

        delete_query = PartSection.__table__.delete().where(PartSection.id.in_(existing_part_sections.values()))
        db.session.execute(delete_query)
        db.session.commit()
