from typing import List, Optional

import aiohttp
import ujson

from fastapi import status, HTTPException
from fastapi.responses import UJSONResponse

from microservices.routes import EMPLOYEE_API, COMPANY_EMPLOYEE_RELATIONSHIP_API
from microservices.dto import CompanyEmployeeRelationshipDTO, EmployeeDTO, EmployeeListDTO


class EmployeeHttpClient:
    @classmethod
    async def get_employee_by_id(cls, employee_id: int) -> EmployeeDTO.Inner:
        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            response = await session.get(EMPLOYEE_API['get'](employee_id))

        result_json = await response.json()

        return EmployeeDTO.Inner.model_validate(result_json)

    @classmethod
    async def employee_exists(cls, employee_id: int) -> bool:
        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            response = await session.head(
                # TODO: переделай типы запросов (head, get) на классы представлющие процессы и состояния
                EMPLOYEE_API['head'],
                json={
                    'employee_id': employee_id,
                },
            )

        if response.status == status.HTTP_200_OK:
            return True
        if response.status == status.HTTP_404_NOT_FOUND:
            return False
        else:
            raise HTTPException(status_code=response.status, detail='Error')

    @classmethod
    async def get_employees(cls, employees_ids: List[int]) -> EmployeeListDTO.Inner:
        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            response = await session.get(
                EMPLOYEE_API['batch'],
                params={
                    'ids': employees_ids,
                }
            )

        if response.status != status.HTTP_200_OK:
            raise HTTPException(status_code=response.status, detail='Company does not have employees 2')

        employees: List[EmployeeDTO.Inner] = []

        for employee in await response.json():
            employee = EmployeeDTO.Inner.model_validate(employee)
            employees.append(employee)

        return EmployeeListDTO.Inner(employees=employees)


class CompanyEmployeeRelationshipHttpClient:
    @classmethod
    async def create(cls, company_employee_relationship: CompanyEmployeeRelationshipDTO) -> UJSONResponse:
        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            response = await session.post(
                COMPANY_EMPLOYEE_RELATIONSHIP_API['create'],
                json=company_employee_relationship.model_dump_json(),
            )

        return UJSONResponse(status_code=response.status, content=await response.json())

    @classmethod
    async def get_employees_ids_by_company_id(cls, company_id: int) -> List[int]:
        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            async with session.get(
                COMPANY_EMPLOYEE_RELATIONSHIP_API['get_employees_ids'](company_id)
            ) as response:
                if response.status == status.HTTP_200_OK:
                    return await response.json()
                if response.status == status.HTTP_404_NOT_FOUND:
                    return []
                raise HTTPException(status_code=response.status, detail=await response.json())


