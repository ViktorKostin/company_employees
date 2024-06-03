import uuid
from typing import Optional

from pydantic import BaseModel, UUID4, field_validator, field_serializer


class EntityBase(BaseModel):
    uuid: Optional[UUID4] = None

    @field_validator('uuid')
    def uuid_encoder(cls, v):
        if v:
            return uuid.UUID(str(v))

    @field_serializer('uuid')
    def uuid_serializer(self, uuid: UUID4):
        return str(self.uuid)

    class Config:
        from_attributes = True


class CompanyEntity(EntityBase):
    id: Optional[int] = None
    name: str


class CompanyDTO(EntityBase):
    name: str
