from uuid import UUID

from pydantic import BaseModel, Field

from api.maps.base import get_new_id
from api.maps.structure.unit import UnitBriefMap


class PartSetSectionMap(BaseModel):
    section_id: UUID = Field(title='Section id')
    order_num: int = Field(title='Section order on the part\'s route')
    is_last_point: bool = Field(title='If section is the last point on the part\'s route')
    cycle_time: int = Field(title='Part production cycle on the current section')
    balance: int = Field(title='Number of Parts storing inside section')


class PartGetSectionMap(PartSetSectionMap):
    section_name: str = Field(title='Section name')


class PartSectionMap(PartSetSectionMap):
    id: UUID = Field(title='PartSection id', default_factory=get_new_id)
    part_id: UUID = Field(title='Part id')


class PartUnitMap(UnitBriefMap):
    quantity: int = Field(title='Number of current part per unit')


class PartOperationMap(BaseModel):
    id: UUID = Field(title='Operation id', default_factory=get_new_id)
    name: str = Field(title='Operation name')
    quantity: int = Field(title='Number of current part per operation')


class PartBriefMap(BaseModel):
    id: UUID = Field(title='Part id', default_factory=get_new_id)
    number: str = Field(title='Part factory number')
    name: str = Field(title='Part name')


class PartFullMap(PartBriefMap):
    sections: list[PartGetSectionMap] = Field(title='Part route')
    units: list[PartUnitMap] = Field(title='Units, that contain the part')
    operations: list[PartOperationMap] = Field(title='Operations, that contain the part')
