from sqlalchemy import Boolean, Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from core.config import CONFIG

from .base import BaseModel


class PartSection(BaseModel):
    __tablename__ = 'part_sections'
    __table_args__ = (
        UniqueConstraint('part_id', 'section_id'),
        {'schema': CONFIG.DB.SCHEMA_NAME},
    )

    part_id = Column(ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.parts.id', ondelete='CASCADE'))
    section_id = Column(ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.sections.id', ondelete='CASCADE'))
    order_num = Column(Integer, default=1)
    is_last_point = Column(Boolean, default=False)
    cycle_time = Column(Integer, default=1)
    balance = Column(Integer, default=0)
    part = relationship('Part', back_populates='sections')
    section = relationship('Section', back_populates='parts')


class UnitSection(BaseModel):
    __tablename__ = 'unit_sections'
    __table_args__ = (
        UniqueConstraint('unit_id', 'section_id'),
        {'schema': CONFIG.DB.SCHEMA_NAME},
    )

    unit_id = Column(ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.units.id', ondelete='CASCADE'))
    section_id = Column(ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.sections.id', ondelete='CASCADE'))
    order_num = Column(Integer, default=1)
    is_last_point = Column(Boolean, default=False)
    cycle_time = Column(Integer, default=1)
    balance = Column(Integer, default=0)
    unit = relationship('Unit', back_populates='sections')
    section = relationship('Section', back_populates='units')


class PartOperation(BaseModel):
    __tablename__ = 'part_operations'
    __table_args__ = (
        UniqueConstraint('part_id', 'operation_id'),
        {'schema': CONFIG.DB.SCHEMA_NAME},
    )

    part_id = Column(ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.parts.id', ondelete='CASCADE'))
    operation_id = Column(ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.operations.id', ondelete='CASCADE'))
    quantity = Column(Integer, nullable=False)
    part = relationship('Part', back_populates='operations')
    operation = relationship('Operation', back_populates='parts')


class PartUnit(BaseModel):
    __tablename__ = 'part_units'
    __table_args__ = (
        UniqueConstraint('part_id', 'unit_id'),
        {'schema': CONFIG.DB.SCHEMA_NAME},
    )

    part_id = Column(ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.parts.id', ondelete='CASCADE'))
    unit_id = Column(ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.units.id', ondelete='CASCADE'))
    quantity = Column(Integer, nullable=False)
    part = relationship('Part', back_populates='units')
    unit = relationship('Unit', back_populates='parts')


class UnitAssociation(BaseModel):
    __tablename__ = 'unit_association'
    __table_args__ = (
        UniqueConstraint('unit_id', 'child_id'),
        {'schema': CONFIG.DB.SCHEMA_NAME},
    )

    unit_id = Column(ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.units.id', ondelete='CASCADE'), primary_key=True)
    child_id = Column(ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.units.id', ondelete='CASCADE'), primary_key=True)
    quantity = Column(Integer(), nullable=False)


class UnitOperation(BaseModel):
    __tablename__ = 'unit_operations'
    __table_args__ = (
        UniqueConstraint('unit_id', 'operation_id'),
        {'schema': CONFIG.DB.SCHEMA_NAME},
    )

    unit_id = Column(ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.units.id', ondelete='CASCADE'))
    operation_id = Column(ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.operations.id', ondelete='CASCADE'))
    quantity = Column(Integer, nullable=False)
    unit = relationship('Unit', back_populates='operations')
    operation = relationship('Operation', back_populates='units')


class OperationProduct(BaseModel):
    __tablename__ = 'operation_products'
    __table_args__ = (
        UniqueConstraint('operation_id', 'product_id'),
        {'schema': CONFIG.DB.SCHEMA_NAME},
    )

    operation_id = Column(ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.operations.id', ondelete='CASCADE'))
    product_id = Column(ForeignKey(f'{CONFIG.DB.SCHEMA_NAME}.products.id', ondelete='CASCADE'))
    is_completed = Column(Boolean, default=False)
    operation = relationship('Operation', back_populates='products')
    product = relationship('Product', back_populates='operations')
