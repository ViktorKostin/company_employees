FROM public.ecr.aws/docker/library/python:3.10-slim

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev --only main

COPY . .

CMD ["poetry", "run", "uvicorn", "company_employee_relationship.main:app", "--host", "0.0.0.0", "--port", "8003"]
