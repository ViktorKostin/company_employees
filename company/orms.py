from uuid import uuid4

from sqlalchemy import BigInteger, UUID
from sqlalchemy.orm import mapped_column, Mapped

from company.infrastucture.database.repositories import Base


class CompanyOrm(Base):
    __tablename__ = 'companies'

    id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True)
    uuid: Mapped[UUID] = mapped_column(UUID, unique=True, default=lambda: uuid4())
    name: Mapped[str]
