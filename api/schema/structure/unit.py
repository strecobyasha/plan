from uuid import UUID

from pydantic import BaseModel, Field

from api.maps.structure.unit import (UnitBriefMap, UnitGetChildrenMap,
                                     UnitGetParentsMap, UnitGetPartMap,
                                     UnitGetSectionMap, UnitOperationMap,
                                     UnitSetPartMap, UnitSetSectionMap,
                                     UnitSetUnitMap)


class CreateUnitBody(BaseModel):
    number: str = Field(title='Unit factory number')
    name: str = Field(title='Unit name')
    sections: list[UnitSetSectionMap] = Field(title='Unit\'s factory route')
    parts: list[UnitSetPartMap] = Field(title='Parts, that the unit contains')
    units: list[UnitSetUnitMap] = Field(title='Units , that the unit contains')


class CreateUnitResponse(BaseModel):
    id: UUID = Field(title='Unit id')
    message: str = Field(title='Response message')


class GetUnitParams(BaseModel):
    id: UUID = Field(title='Unit id')


class GetUnitResponse(BaseModel):
    id: UUID = Field(title='Unit id')
    number: str = Field(title='Unit factory number')
    name: str = Field(title='Unit name')
    sections: list[UnitGetSectionMap] = Field(title='Unit\'s factory route')
    parts: list[UnitGetPartMap] = Field(title='Parts, which the unit contains')
    unit_children: list[UnitGetChildrenMap] = Field(title='Units, which the unit contains')
    unit_parents: list[UnitGetParentsMap] = Field(title='Units, which contain the unit')
    operations: list[UnitOperationMap] = Field(title='Operations, which contain the unit')


class GetUnitsResponse(BaseModel):
    units: list[UnitBriefMap] = Field(title='List of units')


class UpdateUnitParams(BaseModel):
    id: UUID = Field(title='Unit id')


class UpdateUnitBody(CreateUnitBody):
    pass


class UpdateUnitResponse(CreateUnitResponse):
    number: str = Field(title='Unit factory number')
    name: str = Field(title='Unit name')


class DeleteUnitParams(BaseModel):
    id: UUID = Field(title='Unit id')


class DeleteUnitResponse(BaseModel):
    message: str = Field(title='Response message')
