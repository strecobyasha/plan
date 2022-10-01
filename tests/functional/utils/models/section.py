from pydantic import Field

from .base import Base, fake


class Section(Base):
    name: str = Field(default_factory=fake.word)
