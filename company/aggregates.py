from typing import List

import ujson
from fastapi import status
from fastapi.responses import UJSONResponse

from microservices.dto import CompanyEmployeeRelationshipDTO, EmployeeDTO, EmployeeListDTO
from .infrastucture.http.clients import EmployeeHttpClient, CompanyEmployeeRelationshipHttpClient
from .entities import CompanyEntity
from .repositories import CompanyRepository


class CompanyAggregate:
    @classmethod
    async def add_employee(cls, company_id: int, employee_id: int) -> UJSONResponse:
        company_exists: bool = await CompanyRepository.company_exists(company_id)
        employee_exists: bool = await EmployeeHttpClient.employee_exists(employee_id)

        if not company_exists:
            return UJSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'Company not found'})

        if not employee_exists:
            return UJSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'Employee not found'})

        company: CompanyEntity = await CompanyRepository.get_company_by_id(company_id)
        employee: EmployeeDTO.Inner = await EmployeeHttpClient.get_employee_by_id(employee_id)

        response: UJSONResponse = await CompanyEmployeeRelationshipHttpClient.create(
            CompanyEmployeeRelationshipDTO.model_validate(
                {
                    'company_id': company.id,
                    'company_uuid': company.uuid,
                    'employee_id': employee.id,
                    'employee_uuid': employee.uuid,
                }
            )
        )

        return response


    @classmethod
    async def get_employees_by_company_id(cls, company_id: int) -> UJSONResponse:
        company_exists: bool = await CompanyRepository.company_exists(company_id)

        if not company_exists:
            return UJSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'Company not found'})

        employees_ids = await CompanyEmployeeRelationshipHttpClient.get_employees_ids_by_company_id(company_id)

        if employees_ids:
            employees_inner: EmployeeListDTO.Inner = await EmployeeHttpClient.get_employees(employees_ids)
            employees_outer: List[EmployeeDTO.Outer] = [EmployeeDTO.Outer(uuid=emp.uuid, username=emp.username) for emp in employees_inner.employees]
            employees_outer: EmployeeListDTO.Outer = EmployeeListDTO.Outer(employees=employees_outer)

            return UJSONResponse(status_code=status.HTTP_200_OK, content=employees_outer.model_dump())

        return UJSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'Company does not have employees'})