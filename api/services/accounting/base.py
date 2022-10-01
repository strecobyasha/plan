import uuid
from abc import ABC, abstractmethod, abstractproperty
from datetime import date
from http import HTTPStatus

from pydantic.main import ModelMetaclass

from api.errors.structure.base import BaseErrors
from api.models.base import BaseModel
from api.models.models import Section
from api.utils.system import json_abort


class BaseAccountingService(ABC):
    @abstractproperty
    def error(self) -> BaseErrors:
        """Errors"""

    @abstractproperty
    def main_model(self) -> BaseModel:
        """Schema as in database"""

    @abstractproperty
    def history_model(self) -> BaseModel:
        """Schema as in database"""

    @abstractproperty
    def balance_model(self) -> BaseModel:
        """Schema as in database"""

    @abstractproperty
    def map(self) -> ModelMetaclass:
        """Schema as in database"""

    def record(self, item_id: uuid, transfer_date: date, sender_id: uuid, recipient_id: uuid, quantity: int) -> None:
        # Accounting for the transfer.
        obj = self.main_model.query.get(item_id)
        if not obj:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, self.error.NOT_EXISTS)
        if not Section.query.get(sender_id):
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, f'{sender_id}: {self.error.SECTION_NOT_EXISTS}')
        if not Section.query.get(recipient_id):
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, f'{recipient_id}: {self.error.SECTION_NOT_EXISTS}')

        map_data = self.map(**{
            'item_id': item_id,
            'transfer_date': transfer_date,
            'sender_id': sender_id,
            'recipient_id': recipient_id,
            'quantity': quantity,
        })
        element = self.history_model(**map_data.dict())
        element.insert_and_commit()

    @abstractmethod
    def change_balance(self, **kwargs) -> list:
        """ Balance changing. """
