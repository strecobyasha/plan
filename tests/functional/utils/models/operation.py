import random

from pydantic import Field

from .base import Base, fake, get_new_id


class Operation(Base):
    name: str = Field(default_factory=fake.word)
    cycle_time: int = Field(default=1)
    advance: int = Field(default=random.randint(1, 14))
    section_id: str = Field(default=get_new_id())
