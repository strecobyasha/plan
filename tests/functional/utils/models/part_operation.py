from pydantic import Field

from .base import Base, get_new_id


class PartOperation(Base):
    part_id: str = Field(default=get_new_id())
    operation_id: str = Field(default=get_new_id())
    quantity: int = Field(default=1)
