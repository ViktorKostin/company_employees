import uuid
from typing import List

from sqlalchemy import select, exists
from typing_extensions import Self

from company.entities import CompanyEntity
from company.infrastucture.database.tools import new_session
from company.orms import CompanyOrm


class CompanyRepository:
    def __init__(
            self,
            entity: CompanyEntity,
    ):
        self.entity = entity
        self.orm = entity

    def _entity_to_orm(self, entity: CompanyEntity) -> CompanyOrm:
        return CompanyOrm(
            **entity.model_dump()
        )

    @property
    def orm(self):
        return self._orm

    @orm.setter
    def orm(self, var: CompanyEntity | CompanyOrm):
        if isinstance(var, CompanyEntity):
            self._orm = self._entity_to_orm(var)
        if isinstance(var, CompanyOrm):
            self._orm = var

    @classmethod
    async def get_company_by_id(cls, id: int) -> CompanyEntity:
        async with new_session() as session:
            result = await session.get(CompanyOrm, id)

        return CompanyEntity.model_validate(result)

    @classmethod
    async def company_exists(cls, id: int) -> bool:
        stmt = select(exists().where(CompanyOrm.id == id))
        async with new_session() as session:
            result = await session.execute(stmt)

        return result.scalar()

    @classmethod
    async def get_list_companies_by_ids(cls, ids: List[int]) -> List[CompanyEntity]:
        companies = []
        stmt = select(CompanyOrm).filter(CompanyOrm.id.in_(ids))
        async with new_session() as session:
            result = await session.execute(stmt)
        companies_orms = result.scalars().all()

        for company_orm in companies_orms:
            companies.append(CompanyEntity.model_validate(company_orm))

        return companies

    @classmethod
    async def create(cls, company_entity: CompanyEntity) -> Self:
        if not company_entity.uuid:
            company_entity.uuid = uuid.uuid4()

        company_repository = cls(company_entity)
        async with new_session() as session:
            session.add(company_repository.orm)
            await session.commit()
            return company_repository

    @classmethod
    async def get_all_companies(cls) -> List[CompanyEntity]:
        companies: List[CompanyEntity] = []
        stmt = select(CompanyOrm)
        async with new_session() as session:
            result = await session.execute(stmt)

        companies_orm: List[CompanyOrm] = result.scalars().all()

        for company_orm in companies_orm:
            company_entity = CompanyEntity.model_validate(company_orm)
            companies.append(company_entity)

        return companies
