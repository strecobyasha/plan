import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import TIMESTAMP, Column
from sqlalchemy.dialects.postgresql import UUID

from core.config import CONFIG

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True
    __table_args__ = {'schema': CONFIG.DB.SCHEMA_NAME}

    id: uuid = Column(UUID(as_uuid=True), nullable=False, unique=True, primary_key=True)
    created_at: datetime = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: datetime = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def insert_and_commit(self):
        db.session.add(self)
        db.session.commit()
