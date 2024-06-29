from uuid import uuid4

from asyncpg import Connection
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from config_reader import config


class CConnection(Connection):
    def _get_unique_id(self, prefix: str) -> str:
        return f"__asyncpg_{prefix}_{uuid4()}__"


async def setup_get_pool() -> async_sessionmaker:
    engine = create_async_engine(
        f"postgresql+asyncpg://{config.db_user}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_name}?prepared_statement_cache_size=0",
        echo=True,
        pool_pre_ping=True,
        poolclass=NullPool,
        connect_args={
            "statement_cache_size": 0,
            "prepared_statement_cache_size": 0,
            "connection_class": CConnection,
        },
        
    )
    sessionmaker_ = async_sessionmaker(engine, expire_on_commit=False, future=True)

    return sessionmaker_
