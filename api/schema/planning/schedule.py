from pydantic import BaseModel, Field


class CreateScheduleResponse(BaseModel):
    schedule: dict = Field(title='Schedule')
