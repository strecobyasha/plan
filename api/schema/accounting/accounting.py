from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field


class TransferItemBody(BaseModel):
    transfer_date: date = Field(title='Date of the transfer', default=date.today())
    sender_id: UUID = Field(title='Section-producer id')
    recipient_id: UUID = Field(title='Section-consumer id')
    quantity: int = Field(title='Quantity of transferred parts or units')


class TransferItemParams(BaseModel):
    id: UUID = Field(title='Part or unit id')


class TransferItemResponse(BaseModel):
    message: str = Field(title='Response message')


class CompletingOperationBody(BaseModel):
    product_id: UUID = Field(title='Product id')
    completion_date: date = Field(title='Date of the completion', default=date.today())


class CompletingOperationParams(BaseModel):
    id: UUID = Field(title='Operation id')


class CompletingOperationResponse(BaseModel):
    message: str = Field(title='Response message')
