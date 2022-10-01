from typing import Union
from uuid import UUID

from pydantic import BaseModel, Field

from api.maps.base import get_new_id


class OperationSetPartMap(BaseModel):
    part_id: UUID = Field(title='Part id', default_factory=get_new_id)
    quantity: int = Field(title='Number of parts per operation')


class OperationGetPartMap(OperationSetPartMap):
    number: str = Field(title='Part number')
    name: str = Field(title='Part name')


class OperationPartMap(OperationSetPartMap):
    id: UUID = Field(title='PartOperation id', default_factory=get_new_id)
    operation_id: UUID = Field(title='Operation id')


class OperationSetUnitMap(BaseModel):
    unit_id: UUID = Field(title='Unit id', default_factory=get_new_id)
    quantity: int = Field(title='Number of units per operation')


class OperationGetUnitMap(OperationSetUnitMap):
    number: str = Field(title='Unit number')
    name: str = Field(title='Unit name')


class OperationUnitMap(OperationSetUnitMap):
    id: UUID = Field(title='UnitOperation id', default_factory=get_new_id)
    operation_id: UUID = Field(title='Operation id')


class OperationBriefMap(BaseModel):
    id: UUID = Field(title='Operation id', default_factory=get_new_id)
    name: str = Field(title='Operation name')
    cycle_time: int = Field(title='Operation production cycle')
    advance: int = Field(title='Operation advance time relative to the product target time')
    section_id: Union[UUID, None] = Field(title='Operation\'s section id')


class OperationFullMap(OperationBriefMap):
    parts: list[OperationGetPartMap] = Field(title='Parts, that the operation contains')
    units: list[OperationGetUnitMap] = Field(title='Units, that the operation contains')
