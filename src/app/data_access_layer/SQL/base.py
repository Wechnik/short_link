import asyncpg

from typing import Optional

from app.config import PostgresPoolConfig


class AsyncPostgresEngine:
    """Инициализация для асинхронной работы с PostgreSQL."""

    def __init__(self, config: PostgresPoolConfig) -> None:
        self.pool: Optional[asyncpg.pool.Pool] = None
        self._config = config

    async def get_connection_pool(self) -> asyncpg.pool.Pool:
        """Формирует и возвращает пулл коннектов."""
        if not isinstance(self._config, PostgresPoolConfig):
            raise TypeError('Invalid config passed!')
        self.pool = await asyncpg.create_pool(
            dsn=self._create_db_url(),
            min_size=self._config.min_size_pull,
            max_size=self._config.max_size_pull,
        )
        return self.pool

    async def close(self) -> None:
        """Закрывает пулл коннектов."""
        await self.pool.close()

    def _create_db_url(self) -> str:
        """Формирование DSN-строки."""
        return (
            f'postgresql://{self._config.db_user}:{self._config.db_password.get_secret_value()}@'
            f'{self._config.db_host}:{self._config.db_port}/{self._config.db_name}'
        )


async def get_connection_pool():
    """Формирует пулл коннектов."""
    pool = AsyncPostgresEngine(PostgresPoolConfig())
    yield await pool.get_connection_pool()

    await pool.close()
