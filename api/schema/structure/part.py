from uuid import UUID

from pydantic import BaseModel, Field

from api.maps.structure.part import (PartBriefMap, PartGetSectionMap,
                                     PartOperationMap, PartSetSectionMap,
                                     PartUnitMap)


class CreatePartBody(BaseModel):
    number: str = Field(title='Part factory number')
    name: str = Field(title='Part name')
    sections: list[PartSetSectionMap] = Field(title='Part\'s factory route')


class CreatePartResponse(BaseModel):
    id: UUID = Field(title='Part id')
    message: str = Field(title='Response message')


class GetPartParams(BaseModel):
    id: UUID = Field(title='Part id')


class GetPartResponse(BaseModel):
    id: UUID = Field(title='Part id')
    number: str = Field(title='Part factory number')
    name: str = Field(title='Part name')
    sections: list[PartGetSectionMap] = Field(title='Part\'s factory route')
    units: list[PartUnitMap] = Field(title='Units, which contain the part')
    operations: list[PartOperationMap] = Field(title='Operations, which contain the part')


class GetPartsResponse(BaseModel):
    parts: list[PartBriefMap] = Field(title='List of parts')


class UpdatePartParams(BaseModel):
    id: UUID = Field(title='Part id')


class UpdatePartBody(CreatePartBody):
    pass


class UpdatePartResponse(BaseModel):
    id: UUID = Field(title='Part id')
    number: str = Field(title='Part factory number')
    name: str = Field(title='Part name')
    message: str = Field(title='Response message')


class DeletePartParams(BaseModel):
    id: UUID = Field(title='Part id')


class DeletePartResponse(BaseModel):
    message: str = Field(title='Response message')
