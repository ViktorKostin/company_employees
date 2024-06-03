import uuid
from typing import Optional

from pydantic import BaseModel, UUID4, field_serializer, field_validator


class EmployeeEntity(BaseModel):
    id: Optional[int] = None
    uuid: Optional[UUID4] = None
    username: str

    class Config:
        from_attributes = True

    @field_validator('uuid')
    def uuid_encoder(cls, v):
        if v:
            return uuid.UUID(str(v))

    @field_serializer('uuid')
    def uuid_serializer(self, uuid: Optional[UUID4]):
        return str(self.uuid)
