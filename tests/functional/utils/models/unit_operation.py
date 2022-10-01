from pydantic import Field

from .base import Base, get_new_id


class UnitOperation(Base):
    unit_id: str = Field(default=get_new_id())
    operation_id: str = Field(default=get_new_id())
    quantity: int = Field(default=1)
