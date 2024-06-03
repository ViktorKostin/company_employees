from typing import List, Optional

from sqlalchemy import select, exists
from typing_extensions import Self

from .entities import CompanyEmployeeRelationshipEntity as CEREntity
from .infrastucture.database.tools import new_session
from .orms import CompanyEmployeeRelationshipOrm as CEROrm


class CompanyEmployeeRelationRepository:
    _orm: CEROrm
    _entity: CEREntity
    _saved: bool = False

    def __init__(self, entity: Optional[CEREntity] = None):
        if entity:
            self.entity = entity
            self.orm = entity

    @classmethod
    async def create(cls, entity: CEREntity) -> Self:
        repository = cls(entity)
        async with new_session() as session:
            session.add(repository.orm)
            await session.flush()
            result = repository.orm
            if result.id:
                entity = CEREntity.model_validate(result)
                repository.entity = entity
                repository.saved = True
            await session.commit()
        return repository

    @classmethod
    async def relationship_exists(cls, company_id: int, employee_id: int) -> bool:
        stmt = select(
            exists().where(
                CEROrm.company_id == company_id,
                CEROrm.employee_id == employee_id
            )
        )
        async with new_session() as session:
            result = await session.execute(stmt)
        return result.scalar()

    @classmethod
    async def get_employees_ids_by_company_id(cls, company_id: int) -> List[int]:
        stmt = select(CEROrm.employee_id).where(CEROrm.company_id == company_id)
        async with new_session() as session:
            result = await session.execute(stmt)
        return result.scalars().all()

    def _to_orm(self, entity: CEREntity) -> CEROrm:
        return CEROrm(
            company_id=entity.company_id,
            company_uuid=entity.company_uuid,
            employee_id=entity.employee_id,
            employee_uuid=entity.employee_uuid,
        )

    @property
    def orm(self) -> CEROrm:
        return self._orm

    @orm.setter
    def orm(self, entity: CEREntity):
        self._orm = self._to_orm(entity)

    @property
    def entity(self) -> CEREntity:
        return self._entity

    @entity.setter
    def entity(self, entity: CEREntity):
        self._entity = entity

    @property
    def saved(self) -> bool:
        return self._saved

    @saved.setter
    def saved(self, state: bool):
        self._saved = state
