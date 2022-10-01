import uuid
from http import HTTPStatus

from sqlalchemy import or_

from api.errors.structure.unit import UnitErrors
from api.maps.structure.unit import (UnitBriefMap, UnitFullMap,
                                     UnitGetChildrenMap, UnitGetParentsMap,
                                     UnitGetPartMap, UnitGetSectionMap,
                                     UnitOperationMap, UnitPartMap,
                                     UnitSectionMap, UnitSetPartMap,
                                     UnitSetSectionMap, UnitSetUnitMap,
                                     UnitUnitMap)
from api.models.associations import PartUnit, UnitAssociation, UnitSection
from api.models.base import db
from api.models.models import Part, Section, Unit
from api.services.structure.base import BaseService
from api.utils.system import json_abort


class UnitService(BaseService):
    error = UnitErrors
    model = Unit
    map = UnitBriefMap

    def get_item(self, id: uuid) -> UnitFullMap:
        unit = self.model.query.get(id)
        if not unit:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, self.error.NOT_EXISTS)

        children = {}
        parents = {}
        for element in UnitAssociation.query.filter(
                or_(
                    UnitAssociation.unit_id == id,
                    UnitAssociation.child_id == id,
                )
            ):
            children[str(element.child_id)] = element.quantity
            parents[str(element.unit_id)] = element.quantity

        return UnitFullMap(
            **unit.__dict__,
            **{
                'parts': [
                    UnitGetPartMap(
                        part_id=element.part_id,
                        number=element.part.number,
                        name=element.part.name,
                        quantity=element.quantity,
                    )
                    for element in unit.parts
                ],
                'unit_children': [
                    UnitGetChildrenMap(
                        child_id=element.id,
                        number=element.number,
                        name=element.name,
                        quantity=children[str(element.id)],
                    )
                    for element in unit.unit_children
                ],
                'unit_parents': [
                    UnitGetParentsMap(
                        parent_id=element.id,
                        number=element.number,
                        name=element.name,
                        quantity=parents[str(element.id)],
                    )
                    for element in unit.unit_parents
                ],
                'operations': [
                    UnitOperationMap(
                        id=element.operation_id,
                        name=element.operation.name,
                        quantity=element.quantity,
                    )
                    for element in unit.operations
                ],
                'sections': [
                    UnitGetSectionMap(
                        section_id=element.section_id,
                        section_name=element.section.name,
                        order_num=element.order_num,
                        is_last_point=element.is_last_point,
                        cycle_time=element.cycle_time,
                        balance=element.balance,
                    )
                    for element in unit.sections
                ]
            }
        )

    def add_sections(self, unit_id: uuid, sections: list[UnitSetSectionMap]) -> None:
        # Set a route of the unit through the sections.
        existing_part_sections = {
            str(item.section_id): str(item.id)
            for item in UnitSection.query.filter_by(unit_id=unit_id)
        }
        for section in sections:
            map_data = UnitSectionMap(**{'unit_id': unit_id, **section.dict()})
            if str(section.section_id) in existing_part_sections:
                UnitSection.query.filter_by(
                    id=existing_part_sections.pop(str(section.section_id)),
                ).update(map_data.dict())
                db.session.commit()
            elif not Section.query.get(section.section_id):
                json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, f'{section.section_id}: {self.error.SECTION_NOT_EXISTS}')
            else:
                element = UnitSection(**map_data.dict())
                element.insert_and_commit()

        delete_query = UnitSection.__table__.delete().where(UnitSection.id.in_(existing_part_sections.values()))
        db.session.execute(delete_query)
        db.session.commit()

    def add_parts(self, unit_id: uuid, parts: list[UnitSetPartMap]) -> None:
        # Add parts, that the unit contains.
        existing_unit_parts = {
            str(item.part_id): str(item.id)
            for item in PartUnit.query.filter_by(unit_id=unit_id)
        }
        for part in parts:
            map_data = UnitPartMap(**{'unit_id': unit_id, **part.dict()})
            if str(part.part_id) in existing_unit_parts:
                PartUnit.query.filter_by(
                    id=existing_unit_parts.pop(str(part.part_id)),
                ).update(map_data.dict())
                db.session.commit()
            elif not Part.query.get(part.part_id):
                json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, f'{part.part_id}: {self.error.PART_NOT_EXISTS}')
            else:
                element = PartUnit(**map_data.dict())
                element.insert_and_commit()

        delete_query = PartUnit.__table__.delete().where(PartUnit.id.in_(existing_unit_parts.values()))
        db.session.execute(delete_query)
        db.session.commit()

    def add_units(self, unit_id: uuid, units: list[UnitSetUnitMap]) -> None:
        # Add units, that the unit contains.
        existing_unit_units = {
            str(item.child_id): str(item.id)
            for item in UnitAssociation.query.filter_by(unit_id=unit_id)
        }
        for unit in units:
            map_data = UnitUnitMap(**{'unit_id': unit_id, **unit.dict()})
            if str(unit.child_id) in existing_unit_units:
                UnitAssociation.query.filter_by(
                    id=existing_unit_units.pop(str(unit.child_id)),
                ).update(map_data.dict())
                db.session.commit()
            elif not Unit.query.get(unit.child_id):
                json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, f'{unit.child_id}: {self.error.UNIT_NOT_EXISTS}')
            else:
                element = UnitAssociation(**map_data.dict())
                element.insert_and_commit()

        delete_query = UnitAssociation.__table__.delete().where(UnitAssociation.id.in_(existing_unit_units.values()))
        db.session.execute(delete_query)
        db.session.commit()
