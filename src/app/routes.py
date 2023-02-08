from fastapi import FastAPI

from api.v1.create.handler import create_router


def setup_routes_api_v1(app: FastAPI):
    """Единая точка сбора всех эндпоинтов для первой версии api."""
    app.include_router(create_router)
