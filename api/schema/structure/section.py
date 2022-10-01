from uuid import UUID

from pydantic import BaseModel, Field

from api.maps.structure.operation import OperationBriefMap
from api.maps.structure.section import (SectionMap, SectionPartBalanceMap,
                                        SectionPartMap, SectionUnitBalanceMap,
                                        SectionUnitMap)


class CreateSectionBody(BaseModel):
    name: str = Field(title='Section name')


class CreateSectionResponse(BaseModel):
    id: UUID = Field(title='Section id')
    message: str = Field(title='Response message')


class GetSectionParams(BaseModel):
    id: UUID = Field(title='Section id')


class GetSectionResponse(BaseModel):
    id: UUID = Field(title='Section id')
    name: str = Field(title='New section name')


class GetSectionsResponse(BaseModel):
    sections: list[SectionMap] = Field(title='List of sections')


class UpdateSectionParams(BaseModel):
    id: UUID = Field(title='Section id')


class UpdateSectionBody(CreateSectionBody):
    pass


class UpdateSectionResponse(GetSectionResponse):
    message: str = Field(title='Response message')


class DeleteSectionParams(BaseModel):
    id: UUID = Field(title='Section id')


class DeleteSectionResponse(BaseModel):
    message: str = Field(title='Response message')


class SectionPartsParams(BaseModel):
    id: UUID = Field(title='Section id')


class SectionPartsResponse(BaseModel):
    parts: list[SectionPartMap] = Field(title='List of section parts')


class SectionPartsBalanceResponse(BaseModel):
    parts: list[SectionPartBalanceMap] = Field(title='Balance of parts')


class SectionUnitsParams(BaseModel):
    id: UUID = Field(title='Section id')


class SectionUnitsResponse(BaseModel):
    units: list[SectionUnitMap] = Field(title='List of section units')


class SectionUnitsBalanceResponse(BaseModel):
    units: list[SectionUnitBalanceMap] = Field(title='Balance of units')


class SectionOperationsParams(BaseModel):
    id: UUID = Field(title='Section id')


class SectionOperationsResponse(BaseModel):
    operations: list[OperationBriefMap] = Field(title='List of section operations')
