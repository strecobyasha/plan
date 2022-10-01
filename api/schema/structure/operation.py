from typing import Union
from uuid import UUID

from pydantic import BaseModel, Field

from api.maps.structure.operation import (OperationBriefMap,
                                          OperationGetPartMap,
                                          OperationGetUnitMap,
                                          OperationSetPartMap,
                                          OperationSetUnitMap)


class CreateOperationBody(BaseModel):
    name: str = Field(title='Operation name')
    cycle_time: int = Field(title='Operation production cycle')
    advance: int = Field(title='Operation advance time relative to the product target time')
    section_id: UUID = Field(title='Section id')
    parts: list[OperationSetPartMap] = Field(title='Parts, that the operation contains')
    units: list[OperationSetUnitMap] = Field(title='Units , that the operation contains')


class CreateOperationResponse(BaseModel):
    id: UUID = Field(title='Operation id')
    message: str = Field(title='Response message')


class GetOperationParams(BaseModel):
    id: UUID = Field(title='Operation id')


class GetOperationResponse(BaseModel):
    id: UUID = Field(title='Operation id')
    name: str = Field(title='Operation name')
    cycle_time: int = Field(title='Operation production cycle')
    advance: int = Field(title='Operation advance time relative to the product target time')
    section_id: Union[UUID, None] = Field(title='Operation\'s section id')
    parts: list[OperationGetPartMap] = Field(title='Parts, which the operation contains')
    units: list[OperationGetUnitMap] = Field(title='Units, which the operation contains')


class GetOperationsResponse(BaseModel):
    operations: list[OperationBriefMap] = Field(title='List of operations')


class UpdateOperationParams(BaseModel):
    id: UUID = Field(title='Operation id')


class UpdateOperationBody(CreateOperationBody):
    pass


class UpdateOperationResponse(BaseModel):
    id: UUID = Field(title='Operation id')
    name: str = Field(title='Operation name')
    cycle_time: int = Field(title='Operation production cycle')
    advance: int = Field(title='Operation advance time relative to the product target time')
    section_id: UUID = Field(title='Operation\'s section id')
    message: str = Field(title='Response message')


class DeleteOperationParams(BaseModel):
    id: UUID = Field(title='Operation id')


class DeleteOperationResponse(BaseModel):
    message: str = Field(title='Response message')
