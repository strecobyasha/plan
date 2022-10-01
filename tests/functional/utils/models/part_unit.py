from pydantic import Field

from .base import Base, get_new_id


class PartUnit(Base):
    part_id: str = Field(default=get_new_id())
    unit_id: str = Field(default=get_new_id())
    quantity: int = Field(default=1)
