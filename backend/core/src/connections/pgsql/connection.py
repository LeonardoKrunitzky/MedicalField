from contextlib import asynccontextmanager
import os
from typing import Optional, AsyncGenerator

from backend.core.src.connections.base import BaseClient
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text

load_dotenv()

class PostgreSQLClient(BaseClient):
    def __init__(self):
        self._engine: Optional[any] = None
        self._session_factory: Optional[any] = None

    async def connect(self) -> None:
        if self._engine is not None:
            return

        try:
            url=(
                f"postgresql+asyncpg://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}"
            )

            self._engine = create_async_engine(
                url,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
            )

            self._session_factory = async_sessionmaker(
                bind=self._engine,
                autoflush=False,
                expire_on_commit=False,
                class_=AsyncSession,
            )

            print("Connected to PostgreSQL")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to PostgreSQL: {e}")

    async def disconnect(self) -> None:
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._session_factory = None
            print("Disconnected from PostgreSQL")

    async def ensure_connected(self) -> bool:
        try:
            if self._engine is None:
                await self.connect()

            async with self._engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
                return True
        except Exception as e:
            print(f"PostgreSQL connection check failed: {e}")
            return False

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        if self._session_factory is None:
            raise ConnectionError("PostgreSQL session factory is not initialized.")

        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()