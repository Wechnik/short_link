import hashlib

from app.api.v1.create.schemas import RequestCreateShortLink

HOST_NAME = 'https://const.com/'


class CreateShortLink:
    """Создание короткой ссылки."""

    def __init__(self, request: RequestCreateShortLink):
        self._request = request
        self.hash_size = 3

    async def prepare(self):
        """Создаёт короткую ссылку из URL."""
        hasher = hashlib.blake2s(self._request.URL.encode(), digest_size=self.hash_size)
        hash_str = hasher.hexdigest()
        if await self._collision_detector(hash_str):
            return HOST_NAME, hash_str
        self.hash_size += 1
        return await self.prepare()

    async def _collision_detector(self, hash_str: str) -> bool:
        """Проверяет чтобы хеш не повторялся."""
        return True


class DeleteShortLink:
    """Удаление короткой ссылки из памяти."""

    async def prepare(self):
        """Удаляет короткую ссылку по URL."""
        ...


class ReadShortLink:
    """Получает полный URL по короткой ссылке."""

    async def prepare(self, url):
        """Получает полный URL по короткой ссылке."""
        ...
