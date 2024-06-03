from pydantic import BaseModel, UUID4


class CompanyEmployeeRelationshipEntity(BaseModel):
    company_id: int
    company_uuid: UUID4
    employee_id: int
    employee_uuid: UUID4

    class Config:
        from_attributes = True
