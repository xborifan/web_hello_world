from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from web.config import settings


engine = create_async_engine(settings.databaseUrl, echo=True)

async_session_maker = async_sessionmaker(engine,
                                         class_=AsyncSession,
                                         expire_on_commit=False)

class Base(DeclarativeBase):
    metadata = MetaData(schema='public')