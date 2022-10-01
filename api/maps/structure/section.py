import uuid

from pydantic import BaseModel, Field

from api.maps.base import get_new_id
from api.maps.structure.part import PartBriefMap
from api.maps.structure.unit import UnitBriefMap


class SectionMap(BaseModel):
    id: uuid.UUID = Field(title='Section id', default_factory=get_new_id)
    name: str = Field(title='Section name')


class SectionPartMap(PartBriefMap):
    cycle_time: int = Field(title='Part production cycle on the current section')


class SectionPartBalanceMap(PartBriefMap):
    balance: int = Field(title='Number of parts storing inside section')


class SectionUnitMap(UnitBriefMap):
    cycle_time: int = Field(title='Unit production cycle on the current section')


class SectionUnitBalanceMap(UnitBriefMap):
    balance: int = Field(title='Number of units storing inside section')

