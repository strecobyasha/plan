import uuid
from http import HTTPStatus

from api.errors.structure.section import SectionErrors
from api.maps.structure.operation import OperationBriefMap
from api.maps.structure.section import (SectionMap, SectionPartBalanceMap,
                                        SectionPartMap, SectionUnitBalanceMap,
                                        SectionUnitMap)
from api.models.associations import PartSection, UnitSection
from api.models.models import Operation, Section
from api.services.structure.base import BaseService
from api.utils.system import json_abort


class SectionService(BaseService):
    error = SectionErrors
    model = Section
    map = SectionMap

    def get_item(self, id: uuid) -> SectionMap:
        element = self.model.query.get(id)
        if not element:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, self.error.NOT_EXISTS)

        return self.map(**element.__dict__)

    def get_parts(self, section_id: uuid) -> list:
        return [
            SectionPartMap(
                id=element.part_id,
                number=element.part.number,
                name=element.part.name,
                cycle_time=element.cycle_time,
            )
            for element in PartSection.query.filter_by(section_id=section_id, is_last_point=False)
        ]

    def get_parts_balance(self, section_id: uuid) -> list:
        return [
            SectionPartBalanceMap(
                id=element.part_id,
                number=element.part.number,
                name=element.part.name,
                balance=element.balance,
            )
            for element in PartSection.query.filter_by(section_id=section_id)
        ]

    def get_units(self, section_id: uuid) -> list:
        return [
            SectionUnitMap(
                id=element.unit_id,
                number=element.unit.number,
                name=element.unit.name,
                cycle_time=element.cycle_time,
            )
            for element in UnitSection.query.filter_by(section_id=section_id, is_last_point=False)
        ]

    def get_units_balance(self, section_id: uuid) -> list:
        return [
            SectionUnitBalanceMap(
                id=element.unit_id,
                number=element.unit.number,
                name=element.unit.name,
                balance=element.balance,
            )
            for element in UnitSection.query.filter_by(section_id=section_id)
        ]

    def get_operations(self, section_id: uuid) -> list:
        return [
            OperationBriefMap(
                id=element.id,
                name=element.name,
                cycle_time=element.cycle_time,
                advance=element.advance,
                section_id=section_id,
            )
            for element in Operation.query.filter_by(section_id=section_id)
        ]
