from datetime import date

from pydantic import BaseModel, Field


class CreateTablesBodyParams(BaseModel):
    target_date: date = Field(title='Date of month ot the table')


class CreateTablesResponse(BaseModel):
    message: str = Field(title='Response message')
