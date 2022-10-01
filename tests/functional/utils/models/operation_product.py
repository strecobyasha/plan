from pydantic import Field

from .base import Base, get_new_id


class OperationProduct(Base):
    operation_id: str = Field(default=get_new_id())
    product_id: str = Field(default=get_new_id())
    is_completed: bool = Field(default=False)
