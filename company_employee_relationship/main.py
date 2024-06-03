from contextlib import asynccontextmanager

import ujson
from fastapi import FastAPI, APIRouter, Request, status
from fastapi.responses import UJSONResponse

from microservices.dto import CompanyEmployeeRelationshipDTO
from .entities import CompanyEmployeeRelationshipEntity
from .infrastucture.database.repositories import DatabaseRepository
from .repositories import CompanyEmployeeRelationRepository as CERRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    await DatabaseRepository.create_database()
    await DatabaseRepository.create_tables()
    yield
    # await DatabaseRepository.drop_tables()


app = FastAPI(
    title='Company Employee Relationship',
    lifespan=lifespan,
    debug=True,
)

company_employee_relationship_router = APIRouter(prefix='', tags=['api'])


@company_employee_relationship_router.post('/')
async def create(request: Request) -> UJSONResponse:
    data: dict = ujson.loads(await request.json())
    cer_dto = CompanyEmployeeRelationshipDTO.model_validate(data)
    cer_entity = CompanyEmployeeRelationshipEntity.model_validate(cer_dto.model_dump())
    relationship_exists: bool = await CERRepository.relationship_exists(cer_entity.company_id, cer_entity.employee_id)
    if relationship_exists:
        return UJSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': 'Company already have employee'})

    cer_repository = await CERRepository.create(cer_entity)

    if cer_repository.saved:
        return UJSONResponse(status_code=status.HTTP_201_CREATED, content={'detail': 'Employee added'})
    return UJSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'detail': 'Error'})


@company_employee_relationship_router.get('/{company_id}')
async def get_employees_ids_by_company_id(company_id: int) -> UJSONResponse:
    result = await CERRepository.get_employees_ids_by_company_id(company_id)
    if result:
        return UJSONResponse(status_code=status.HTTP_200_OK, content=result)
    return UJSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'Company does not have employees'})


app.include_router(
    company_employee_relationship_router,
)
