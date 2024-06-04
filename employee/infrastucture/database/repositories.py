from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import settings

aengine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False,
)


class BaseOrm(DeclarativeBase):
    pass


class DatabaseRepository:
    BaseOrmClass: DeclarativeBase = BaseOrm

    @classmethod
    async def create_database(cls):
        tmp_aengine = create_async_engine(settings.URL_FOR_CREATION_DATABASE)
        async with tmp_aengine.connect() as conn:
            try:
                autocommit = await conn.execution_options(isolation_level="AUTOCOMMIT")
                await autocommit.execute(text(f'CREATE DATABASE {settings.DB_NAME}'))
            except Exception as e:
                print('notification:', e)

    @classmethod
    async def create_tables(cls):
        async with aengine.connect() as conn:
            await conn.run_sync(cls.BaseOrmClass.metadata.create_all)
            await conn.commit()

    @classmethod
    async def drop_tables(cls):
        async with aengine.connect() as conn:
            await conn.run_sync(cls.BaseOrmClass.metadata.drop_all)
            await conn.commit()

    @classmethod
    async def drop_and_create_tables(cls):
        database = cls()
        await database.drop_tables()
        await database.create_tables()
