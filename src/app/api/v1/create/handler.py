import asyncpg
import validators
from fastapi import APIRouter, HTTPException, Depends

from app.api.v1.create.schemas import ResponseCreateShortLink, RequestCreateShortLink
from app.data_access_layer.SQL.base import get_connection_pool
from app.data_access_layer.SQL.data_access_object import CreateEntry
from app.main.main import CreateShortLink

create_router = APIRouter()


@create_router.post("/api/v1/create/", response_model=ResponseCreateShortLink)
async def post(request: RequestCreateShortLink, pool: asyncpg.pool.Pool = Depends(get_connection_pool)):
    """Эндпоинт для формирования ссылки."""
    if validators.url(request.URL):
        host, hash_ = await CreateShortLink(request).prepare()
        await CreateEntry().create(request.URL, hash_, pool)
        return ResponseCreateShortLink(short_URL=host+hash_)
    raise HTTPException(status_code=400, detail="Not found url in request!")
