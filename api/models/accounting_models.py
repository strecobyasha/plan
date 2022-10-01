import uuid
from datetime import date, datetime, timedelta

from sqlalchemy import (TIMESTAMP, Column, Date, ForeignKey, Integer,
                        UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr

from core.config import CONFIG

from .base import BaseModel, db


class BaseAccountingModel(BaseModel):
    __abstract__ = True

    @classmethod
    def create_partition(self, target_date: date, table_name: str) -> None:
        name = f'{CONFIG.DB.SCHEMA_NAME}.{table_name}_{target_date.strftime("%m_%Y")}'

        start = datetime.strptime(
            f'{target_date.replace(day=1)}T{datetime.min.time()}', '%Y-%m-%dT%H:%M:%S'
        ).astimezone()

        end = datetime.strptime(
            f'{(target_date.replace(day=28) + timedelta(days=4)).replace(day=1)}T{datetime.min.time()}',
            '%Y-%m-%dT%H:%M:%S',
        ).astimezone()

        query = (
            "CREATE TABLE IF NOT EXISTS %(name)s "
            "PARTITION OF %(schema)s.%(table)s "
            "FOR VALUES FROM ('%(start)s') TO ('%(end)s');"
        )
        params = {
            'name': name,
            'schema': CONFIG.DB.SCHEMA_NAME,
            'table': table_name,
            'start': start,
            'end': end,
        }

        db.session.execute(query % params)
        db.session.commit()


class ItemTransferHistory(BaseAccountingModel):
    __abstract__ = True

    __table_args__ = (
        UniqueConstraint('id', 'transfer_date'),
        {'schema': CONFIG.DB.SCHEMA_NAME, 'postgresql_partition_by': 'RANGE (transfer_date)'},
    )

    id: uuid = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    transfer_date = Column(Date(), nullable=False, default=date.today, primary_key=True)
    quantity = Column(Integer, default=0)

    @declared_attr
    def sender_id(cls):
        return Column(ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.sections.id', ondelete='CASCADE'))

    @declared_attr
    def recipient_id(cls):
        return Column(ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.sections.id', ondelete='CASCADE'))


class PartsTransferHistory(ItemTransferHistory):
    __tablename__ = 'parts_transfer_history'

    item_id = Column(ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.parts.id', ondelete='CASCADE'))


class UnitsTransferHistory(ItemTransferHistory):
    __tablename__ = 'units_transfer_history'

    item_id = Column(ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.units.id', ondelete='CASCADE'))


class OperationsHistory(BaseAccountingModel):
    __tablename__ = 'operations_history'
    __table_args__ = (
        UniqueConstraint('id', 'completion_date'),
        {'schema': CONFIG.DB.SCHEMA_NAME, 'postgresql_partition_by': 'RANGE (completion_date)'},
    )

    id: uuid = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    operation_id = Column(ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.operations.id', ondelete='CASCADE'))
    product_id = Column(ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.products.id', ondelete='CASCADE'))
    completion_date: date = Column(Date(), nullable=False, default=date.today, primary_key=True)
