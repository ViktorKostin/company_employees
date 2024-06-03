import uuid
from typing import Optional, List

from sqlalchemy import select, exists
from typing_extensions import Self

from .entities import EmployeeEntity
from .infrastucture.database.tools import new_session
from .orms import EmployeeOrm


class EmployeeRepository:
    _entity: EmployeeEntity
    _orm: EmployeeOrm

    def __init__(self, employee_entity: Optional[EmployeeEntity]):
        if employee_entity:
            self._entity = employee_entity
            self.orm = employee_entity

    @property
    def orm(self) -> EmployeeOrm:
        return self._orm

    @orm.setter
    def orm(self, entity: EmployeeEntity):
        self._orm = self._to_orm(entity)

    @property
    def entity(self) -> EmployeeEntity:
        return self._entity

    @entity.setter
    def entity(self, orm: EmployeeOrm):
        self._entity = self._to_entity(orm)

    def _to_orm(self, entity: EmployeeEntity) -> EmployeeOrm:
        return EmployeeOrm(**entity.model_dump())

    def _to_entity(self, orm: EmployeeOrm) -> EmployeeEntity:
        return EmployeeEntity.model_validate(orm)

    @classmethod
    async def get_employee_by_id(cls, id: int) -> Optional[EmployeeEntity]:
        async with new_session() as session:
            orm = await session.get(EmployeeOrm, id)
            if orm is not None:
                return EmployeeEntity.model_validate(orm)
        return None

    @classmethod
    async def get_batch_employees_by_ids(cls, ids: List[int]) -> List[EmployeeEntity]:
        employees: List[EmployeeEntity] = []
        stmt = select(EmployeeOrm).filter(EmployeeOrm.id.in_(ids))
        async with new_session() as session:
            result = await session.execute(stmt)
            employees_orm = result.scalars().all()

        for employee_orm in employees_orm:
            employees.append(EmployeeEntity.model_validate(employee_orm))

        return employees

    @classmethod
    async def get_all_employees(cls) -> List[EmployeeEntity]:
        employees: List[EmployeeEntity] = []
        stmt = select(EmployeeOrm)
        async with new_session() as session:
            result = await session.execute(stmt)

        employees_orms = result.scalars().all()

        for employee_orm in employees_orms:
            employee_entity = EmployeeEntity.model_validate(employee_orm)
            employees.append(employee_entity)

        return employees

    @classmethod
    async def employee_exists(cls, employee_id) -> bool:
        stmt = select(exists().where(EmployeeOrm.id == employee_id))
        async with new_session() as session:
            result = await session.execute(stmt)

        return result.scalar()

    @classmethod
    async def create(cls, employee_entity: EmployeeEntity) -> Self:
        if not employee_entity.uuid:
            employee_entity.uuid = uuid.uuid4()

        employee_repository = cls(employee_entity)
        async with new_session() as session:
            session.add(employee_repository.orm)
            await session.commit()
            return employee_repository
