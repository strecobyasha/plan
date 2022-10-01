from pydantic import Field

from .base import Base, get_new_id


class UnitSection(Base):
    unit_id: str = Field(default=get_new_id())
    section_id: str = Field(default=get_new_id())
    order_num: int = Field(default=1)
    is_last_point: bool = Field(default=False)
    cycle_time: int = Field(default=1)
    balance: int = Field(default=0)
