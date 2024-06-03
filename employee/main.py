from contextlib import asynccontextmanager
from typing import Annotated, List, Optional

from fastapi import FastAPI, Depends, Query, APIRouter, status
from fastapi.params import Body
from fastapi.responses import UJSONResponse, Response

from .entities import EmployeeEntity
from .infrastucture.database.repositories import DatabaseRepository
from .repositories import EmployeeRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    await DatabaseRepository.create_database()
    await DatabaseRepository.create_tables()
    yield
    # await database_repository.drop_tables()


app = FastAPI(
    title='Employee',
    lifespan=lifespan,
)

employee_router = APIRouter(prefix='', tags=['api'])


@employee_router.post('/')
async def create(employee: Annotated[EmployeeEntity, Depends(EmployeeEntity)]):
    await EmployeeRepository.create(employee)
    return UJSONResponse(status_code=status.HTTP_201_CREATED, content={'detail': 'Employee created'})


@employee_router.get('/{id}')
async def get_employee_by_id(id: int) -> UJSONResponse:
    entity: Optional[EmployeeEntity] = await EmployeeRepository.get_employee_by_id(id)
    if entity:
        return UJSONResponse(status_code=status.HTTP_200_OK, content=entity.model_dump())
    return UJSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'Employee not exists'})


@employee_router.get('/batch/')
async def get_batch_employees_by_ids(ids: List[int] = Query()) -> UJSONResponse:
    employees: List[EmployeeEntity] = await EmployeeRepository.get_batch_employees_by_ids(ids)
    if employees:
        json_employees = []
        for employee in employees:
            json_employees.append(employee.model_dump())
        return UJSONResponse(status_code=status.HTTP_200_OK, content=json_employees)
    return UJSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='Company does not have employees')


@employee_router.get('/')
async def get_all_employees() -> List[EmployeeEntity]:
    return await EmployeeRepository.get_all_employees()


@employee_router.head('/')
async def employee_exists(body: Annotated[dict, Body()]):
    employee_id: int = body['employee_id']
    employee_exists: bool = await EmployeeRepository.employee_exists(employee_id)
    if employee_exists:
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_404_NOT_FOUND)


app.include_router(
    employee_router,
)
