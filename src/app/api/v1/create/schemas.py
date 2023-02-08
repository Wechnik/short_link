from pydantic import BaseModel


class RequestCreateShortLink(BaseModel):
    """Схема на создание короткой ссылки."""

    URL: str


class ResponseCreateShortLink(BaseModel):
    """Схема ответа при создании короткой ссылки."""

    short_URL: str
