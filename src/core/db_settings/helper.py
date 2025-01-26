from asyncio import current_task
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine
)


class DatabaseHelper:

    def __init__(self):
        self.engine = create_async_engine(
            url='sqlite+aiosqlite:///./db.sqlite3'
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            expire_on_commit=False
        )

    def get_scoped_session(self):
        return async_scoped_session(
            self.session_factory,
            current_task
        )

    async def session_dependency(self) -> AsyncGenerator[AsyncSession]:
        session = self.get_scoped_session()
        try:
            yield session
        finally:
            await session.remove()


db_helper = DatabaseHelper()
