import uuid
from datetime import datetime

from faker import Faker
from pydantic import BaseModel, Field

fake = Faker()


def get_new_id() -> str:
    return str(uuid.uuid4())


def get_datetime() -> str:
    return str(datetime.utcnow())


class Base(BaseModel):
    id: str = Field(default_factory=get_new_id)
    created_at: str = Field(default=get_datetime())
    updated_at: datetime = Field(default=get_datetime())
