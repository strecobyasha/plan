from uuid import UUID

from pydantic import BaseModel, Field

from api.maps.base import get_new_id


class UnitSetSectionMap(BaseModel):
    section_id: UUID = Field(title='Section id')
    order_num: int = Field(title='Section order on the unit\'s route')
    is_last_point: bool = Field(title='If section is the last point on the unit\'s route')
    cycle_time: int = Field(title='Unit production cycle on the current section')
    balance: int = Field(title='Number of units storing inside section')


class UnitGetSectionMap(UnitSetSectionMap):
    section_name: str = Field(title='Section name')


class UnitSectionMap(UnitSetSectionMap):
    id: UUID = Field(title='UnitSection id', default_factory=get_new_id)
    unit_id: UUID = Field(title='Unit id')


class UnitSetPartMap(BaseModel):
    part_id: UUID = Field(title='Part id', default_factory=get_new_id)
    quantity: int = Field(title='Number of parts per unit')


class UnitGetPartMap(UnitSetPartMap):
    number: str = Field(title='Part number')
    name: str = Field(title='Part name')


class UnitPartMap(UnitSetPartMap):
    id: UUID = Field(title='PartUnit id', default_factory=get_new_id)
    unit_id: UUID = Field(title='Unit id')


class UnitSetUnitMap(BaseModel):
    child_id: UUID = Field(title='Unit id', default_factory=get_new_id)
    quantity: int = Field(title='Number of parts per unit')


class UnitGetChildrenMap(UnitSetUnitMap):
    number: str = Field(title='Unit number')
    name: str = Field(title='Unit name')


class UnitGetParentsMap(BaseModel):
    parent_id: UUID = Field(title='Unit id', default_factory=get_new_id)
    number: str = Field(title='Unit number')
    name: str = Field(title='Unit name')
    quantity: int = Field(title='Number of parts per unit')


class UnitUnitMap(UnitSetUnitMap):
    id: UUID = Field(title='Unit id', default_factory=get_new_id)
    unit_id: UUID = Field(title='Unit id')


class UnitOperationMap(BaseModel):
    id: UUID = Field(title='Operation id', default_factory=get_new_id)
    name: str = Field(title='Operation name')
    quantity: int = Field(title='Number of current unit per operation')


class UnitBriefMap(BaseModel):
    id: UUID = Field(title='Unit id', default_factory=get_new_id)
    number: str = Field(title='Unit factory number')
    name: str = Field(title='Unit name')


class UnitFullMap(UnitBriefMap):
    sections: list[UnitGetSectionMap] = Field(title='Unit route')
    parts: list[UnitGetPartMap] = Field(title='Parts, that the unit contains')
    unit_children: list[UnitGetChildrenMap] = Field(title='Units, that the unit contains')
    unit_parents: list[UnitGetParentsMap] = Field(title='Units, that contain the unit')
    operations: list[UnitOperationMap] = Field(title='Operations, that contain the unit')
