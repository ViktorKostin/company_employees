from sqlalchemy import BigInteger, UUID
from sqlalchemy.orm import Mapped, mapped_column

from .infrastucture.database.repositories import BaseOrm


class CompanyEmployeeRelationshipOrm(BaseOrm):
    __tablename__ = 'companies_employees_relationship'

    id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True)
    company_id: Mapped[BigInteger] = mapped_column(BigInteger)
    company_uuid: Mapped[UUID] = mapped_column(UUID)
    employee_id: Mapped[BigInteger] = mapped_column(BigInteger)
    employee_uuid: Mapped[UUID] = mapped_column(UUID)
