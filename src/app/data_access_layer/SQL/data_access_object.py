from datetime import datetime
from typing import Optional

import asyncpg


class CreateEntry:
    """Создание записей в базу."""

    async def create(
        self,
        url: str,
        hash_: str,
        pool: asyncpg.pool.Pool,
    ) -> None:
        """Метод для формирования записи о ссылке в БД."""
        async with pool.acquire() as con:
            await con.execute(f"""
                INSERT INTO short_link("hash", "link", "created_at") 
                VALUES ('{hash_}', '{url}', '{datetime.utcnow()}');
            """)


class ReadEntry:
    """Класс для чтения записей."""

    async def read_by_hash(self, hash_: str, pool: asyncpg.pool.Pool) -> Optional[str]:
        """Метод поиска записей по хешу."""
        async with pool.acquire() as con:
            item = await con.fetch(f"""
                SELECT link FROM short_link WHERE hash = '{hash_}';
            """)
            if item:
                return item[0]['link']

    async def is_url_in_db(self, url: str, pool: asyncpg.pool.Pool) -> list:
        """Метод поиска записей по url для исключения дублирования."""
        async with pool.acquire() as con:
            item = await con.fetch(f"""
                SELECT hash FROM short_link WHERE link = '{url}';
            """)
            return item


class DeleteEntry:
    """Удаление записи из БД."""

    async def delete(
        self,
        hash_: str,
        pool: asyncpg.pool.Pool,
    ) -> bool:
        """Метод для удаления из БД."""
        async with pool.acquire() as con:
            item = await con.fetch(f"""
                DELETE FROM short_link WHERE hash = '{hash_}';
            """)
        return bool(item)


class CRUD:
    """Фасад для операций CRUD в БД."""

    def __init__(self, pool: asyncpg.pool.Pool):
        self._create = CreateEntry()
        self._read = ReadEntry()
        self._delete = DeleteEntry()
        self._pool = pool

    async def create(
        self,
        url: str,
        hash_: str,
    ) -> Optional[str]:
        """Добавление ссылки в БД."""
        item = await self._read.is_url_in_db(url, self._pool)
        if bool(item):
            return item[0]['hash']
        await self._create.create(url, hash_, self._pool)

    async def read(self, hash_: str) -> Optional[str]:
        """Поиск ссылки в БД."""
        return await self._read.read_by_hash(hash_, self._pool)

    async def delete(self, hash_: str):
        """Удаление ссылки."""
        return await self._delete.delete(hash_, self._pool)
