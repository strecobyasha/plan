from sqlalchemy import (Column, Date, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.config import CONFIG

from .base import BaseModel


class Section(BaseModel):
    __tablename__ = 'sections'

    name = Column(String(255), unique=True, nullable=False)
    parts = relationship('PartSection', back_populates='section', cascade='all, delete')
    units = relationship('UnitSection', back_populates='section', cascade='all, delete')
    operations = relationship('Operation', back_populates='section')


class Part(BaseModel):
    __tablename__ = 'parts'

    number = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    units = relationship('PartUnit', back_populates='part', cascade='all, delete')
    operations = relationship('PartOperation', back_populates='part', cascade='all, delete')
    sections = relationship('PartSection', back_populates='part', cascade='all, delete')


class Unit(BaseModel):
    __tablename__ = 'units'

    number = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    parts = relationship('PartUnit', back_populates='unit', cascade='all, delete')
    unit_children = relationship(
        'Unit',
        secondary=f'{CONFIG.DB.SCHEMA_NAME}.unit_association',
        primaryjoin=f'Unit.id == UnitAssociation.unit_id',
        secondaryjoin=f'Unit.id == UnitAssociation.child_id',
        backref='unit_parents',
        cascade='all, delete',
    )
    operations = relationship('UnitOperation', back_populates='unit', cascade='all, delete')
    sections = relationship('UnitSection', back_populates='unit', cascade='all, delete')


class Operation(BaseModel):
    __tablename__ = 'operations'

    name = Column(String(255), unique=True, nullable=False)
    cycle_time = Column(Integer, nullable=False)
    advance = Column(Integer, nullable=False)
    section_id = Column(UUID(as_uuid=True), ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.sections.id', ondelete='SET NULL'))
    parts = relationship('PartOperation', back_populates='operation', cascade='all, delete')
    units = relationship('UnitOperation', back_populates='operation', cascade='all, delete')
    section = relationship('Section', back_populates='operations')
    products = relationship('OperationProduct', back_populates='operation', cascade='all, delete')


class Product(BaseModel):
    __tablename__ = 'products'
    __table_args__ = (
        UniqueConstraint('number', 'name', 'customer', 'contract'),
        {'schema': CONFIG.DB.SCHEMA_NAME},
    )

    number = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    customer = Column(String(255), nullable=False)
    contract = Column(String(255), nullable=False)
    delivery_date = Column(Date, nullable=False)
    operations = relationship('OperationProduct', back_populates='product', cascade='all, delete')
