from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field

from api.maps.base import get_new_id


class ItemTransferMap(BaseModel):
    id: UUID = Field(title='TransferHistory id', default_factory=get_new_id)
    transfer_date: date = Field(title='Date of the transfer', default=date.today())
    item_id: UUID = Field(title='Part or unit id')
    sender_id: UUID = Field(title='Section-producer id')
    recipient_id: UUID = Field(title='Section-consumer id')
    quantity: int = Field(title='Quantity of transferred parts or units')


class OperationCompletingMap(BaseModel):
    id: UUID = Field(title='OperationsHistory id', default_factory=get_new_id)
    completion_date: date = Field(title='Date of the completion', default=date.today())
    operation_id: UUID = Field(title='Operation id')
    product_id: UUID = Field(title='Product id')
