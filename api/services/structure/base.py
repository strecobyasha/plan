import uuid
from abc import ABC, abstractmethod, abstractproperty
from http import HTTPStatus

from pydantic.main import ModelMetaclass
from sqlalchemy import exc

from api.errors.structure.base import BaseErrors
from api.models.base import BaseModel, db
from api.utils.system import json_abort


class BaseService(ABC):
    @abstractproperty
    def map(self) -> ModelMetaclass:
        """Schema as in database"""

    @abstractproperty
    def model(self) -> BaseModel:
        """Schema as in database"""

    @abstractproperty
    def error(self) -> BaseErrors:
        """Errors"""

    def create(self, **kwargs) -> uuid:
        map_data = self.map(**kwargs)
        element = self.model(**map_data.dict())
        try:
            element.insert_and_commit()
        except exc.IntegrityError:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, self.error.ALREADY_EXISTS)

        return element.id

    @abstractmethod
    def get_item(self, id: uuid) -> ModelMetaclass:
        """ Get element. """

    def get_list(self) -> list[ModelMetaclass]:
        """ Get all elements. """
        return [
            self.map(**item.__dict__)
            for item in self.model.query.all()
        ]

    def update(self, id: uuid, **kwargs) -> ModelMetaclass:
        element = self.model.query.get(id)
        if not element:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, self.error.NOT_EXISTS)
        map_data = self.map(id=id, **kwargs)
        self.model.query.filter_by(id=id).update(map_data.dict())
        db.session.commit()

        return map_data

    def delete(self, id: uuid) -> None:
        elem = self.model.query.get(id)
        if not elem:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, self.error.NOT_EXISTS)

        db.session.delete(elem)
        db.session.commit()
