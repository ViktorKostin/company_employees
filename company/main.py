from contextlib import asynccontextmanager
from typing import Annotated, List

from fastapi import FastAPI, Depends, Query, APIRouter, HTTPException, Header, status
from fastapi.responses import UJSONResponse

from .aggregates import CompanyAggregate
from .entities import CompanyEntity, CompanyDTO
from .infrastucture.database.repositories import DatabaseRepository
from .repositories import CompanyRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    await DatabaseRepository.create_database()
    await DatabaseRepository.create_tables()
    yield
    # await database_repository.drop_tables()


app = FastAPI(
    title='Company',
    lifespan=lifespan,
)

company_router = APIRouter(prefix='', tags=['api'])


@company_router.post('/')
async def create(company: Annotated[CompanyEntity, Depends(CompanyEntity)]):
    await CompanyRepository.create(company)
    return UJSONResponse(status_code=status.HTTP_201_CREATED, content={'detail': 'Company has been created'})


@company_router.get('/{id}', response_model=CompanyDTO)
async def get_company_by_id(id: int) -> CompanyEntity:
    return await CompanyRepository.get_company_by_id(id)


@company_router.get('/', response_model=List[CompanyDTO])
async def get_all_companies() -> List[CompanyEntity]:
    return await CompanyRepository.get_all_companies()


@company_router.get('/batch/', response_model=List[CompanyDTO])
async def get_batch_employees_by_ids(ids: List[int] = Query(alias="ids", convert_underscores=False)) -> List[
    CompanyEntity]:
    return await CompanyRepository.get_list_companies_by_ids(ids)


@company_router.post('/employee')
async def add_employee_to_company(company_id: int, employee_id: int) -> UJSONResponse:
    response: UJSONResponse = await CompanyAggregate.add_employee(company_id, employee_id)
    if response.status_code == status.HTTP_201_CREATED:
        return UJSONResponse(status_code=status.HTTP_200_OK, content={'detail': 'Employee added to company'})
    else:
        return response


@company_router.get('/employees/{company_id}')
async def get_company_employees(company_id: int) -> UJSONResponse:
    return await CompanyAggregate.get_employees_by_company_id(company_id)


app.include_router(
    company_router,
)
