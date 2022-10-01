import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from psycopg2.extras import DictCursor, execute_values
from pydantic.main import ModelMetaclass

from ...settings import CONFIG


class BaseDataGenerator(ABC):
    """Fake data for tests"""

    def __init__(self, conn: DictCursor) -> None:
        self.conn = conn
        self.data = []

    @property
    @abstractmethod
    def table(self) -> str:
        """Table name"""

    @property
    @abstractmethod
    def fake_model(self) -> ModelMetaclass:
        """Fake model"""

    async def load(self) -> list[dict]:
        """Upload fake data"""
        data_to_upload: list[ModelMetaclass] = []

        with open(f'{CONFIG.BASE_DIR}/test_data/{self.table}.json', 'r') as fd:
            fake_data = json.load(fd)

        for elem in fake_data:
            model = self.fake_model.parse_obj(elem)
            data_to_upload.append(model)

        self.data = self._data_wrapper(fake_docs=data_to_upload)

        into_statement: list[str] = [field for field in model.dict().keys()]
        insert_query: str = (
            f'INSERT INTO {CONFIG.DB.SCHEMA_NAME}.{self.table}'
            f'({", ".join(into_statement)}) '
            f'VALUES %s ON CONFLICT DO NOTHING'
        )

        execute_values(
            self.conn,
            insert_query,
            (self._get_values_statement(into_statement=into_statement, data=elem) for elem in self.data),
        )
        self.conn.execute('COMMIT;')

        return self.data

    async def clean(self) -> None:
        """Remove fake data"""
        ids: list[list] = [[elem['id'] for elem in self.data]]
        delete_query: str = (f'DELETE FROM {CONFIG.DB.SCHEMA_NAME}.{self.table} ' f'WHERE id in %s')
        execute_values(self.conn, delete_query, ids)
        self.conn.execute('COMMIT;')

    def _get_values_statement(self, into_statement: list[str], data: dict[str, Any]) -> tuple[Any]:
        return tuple(data[key] for key in into_statement)

    def _data_wrapper(self, fake_docs: list[ModelMetaclass]) -> list[dict[str, Any]]:
        return [
            {**doc.dict(), 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()}
            for doc in fake_docs
        ]
