import re
import uuid
from typing import List

from pydantic import BaseModel, UUID4, field_validator, field_serializer


class CompanyEmployeeRelationshipDTO(BaseModel):
    company_id: int
    company_uuid: UUID4
    employee_id: int
    employee_uuid: UUID4

    @field_validator('company_uuid', 'employee_uuid')
    def uuid_encoder(cls, v):
        return uuid.UUID(str(v))


class EmployeeDTO(BaseModel):
    class Outer(BaseModel):
        uuid: UUID4
        username: str

        @field_validator('uuid')
        def uuid_encoder(cls, v):
            if v:
                return uuid.UUID(str(v))

        @field_serializer('uuid')
        def uuid_serialize(self, uuid: UUID4):
            return str(self.uuid)

    class Inner(Outer):
        id: int


class EmployeeListDTO(BaseModel):
    class Outer(BaseModel):
        employees: List[EmployeeDTO.Outer]

    class Inner(BaseModel):
        employees: List[EmployeeDTO.Inner]
