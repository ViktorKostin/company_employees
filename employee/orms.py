from uuid import uuid4

from sqlalchemy import BigInteger, UUID
from sqlalchemy.orm import Mapped, mapped_column

from .infrastucture.database.repositories import BaseOrm


class EmployeeOrm(BaseOrm):
    __tablename__ = 'employees'

    id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True)
    uuid: Mapped[UUID] = mapped_column(UUID, unique=True, default=lambda: uuid4())
    username: Mapped[str]
