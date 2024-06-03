#### Description
Asynchronous microservice oriented architecture partly founded on DDD principles. <br>

3 microservices:
- company
- employee
- company employee relationship

technologies:
- fastapi
- aiohttp
- docker (and docker-compose)
- sqlalchemy
- pydantic
- postgresql (only 1 instance with 3 databases, just for demonstration other principles)


#### Deploy
```bash
docker compose up --build
```

#### Endpoints
- http://127.0.0.1:8002/docs/ - company
- http://127.0.0.1:8001/docs/ - employee
- http://127.0.0.1:8003/docs/ - companies to employees relationship
