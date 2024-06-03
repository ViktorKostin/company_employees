EMPLOYEE_PORT = 8001
EMPLOYEE_URL = f'http://employee:{EMPLOYEE_PORT}'
EMPLOYEE_API = {
    'url': EMPLOYEE_URL,
    'create': EMPLOYEE_URL + '/',
    'get': lambda id: EMPLOYEE_URL + f'/{id}',
    'all': EMPLOYEE_URL + '/',
    'head': EMPLOYEE_URL + '/',
    'batch': EMPLOYEE_URL + '/batch/',
}

COMPANY_PORT = 8002
COMPANY_URL = f'http://company:{COMPANY_PORT}'
COMPANY_API = {
    'url': COMPANY_URL,
    'create': COMPANY_URL + '/',
    'get': lambda company_id: COMPANY_URL + f'/{company_id}',
    'all': COMPANY_URL + '/',
    'batch': COMPANY_URL + '/batch/',
}

COMPANY_EMPLOYEE_RELATIONSHIP_PORT = 8003
COMPANY_EMPLOYEE_RELATIONSHIP_URL = f'http://company_employee_relationship:{COMPANY_EMPLOYEE_RELATIONSHIP_PORT}'
COMPANY_EMPLOYEE_RELATIONSHIP_API = {
    'url': COMPANY_EMPLOYEE_RELATIONSHIP_URL,
    'create': COMPANY_EMPLOYEE_RELATIONSHIP_URL + '/',
    'get_employees_ids': lambda company_id: COMPANY_EMPLOYEE_RELATIONSHIP_URL + f'/{company_id}',
}

