from datetime import date

from pydantic import Field

from .base import Base, fake


class Product(Base):
    number: str = Field(default_factory=fake.isbn10)
    name: str = Field(default_factory=fake.word)
    customer: str = Field(default_factory=fake.company)
    contract: str = Field(default_factory=fake.ssn)
    delivery_date: date = Field(default_factory=fake.date)
