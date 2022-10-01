from pydantic import Field

from .base import Base, fake


class Part(Base):
    number: str = Field(default_factory=fake.isbn10)
    name: str = Field(default_factory=fake.word)
