from sqlalchemy.ext.asyncio import async_sessionmaker

from .repositories import aengine

new_session = async_sessionmaker(aengine)
