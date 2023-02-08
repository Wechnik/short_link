import uvicorn
from fastapi import FastAPI

from routes import setup_routes_api_v1



app = FastAPI()


@app.on_event('startup')
async def startup():
    ...


@app.on_event("shutdown")
async def shutdown():
    ...


def start_service():
    """Запуск сервиса."""
    setup_routes_api_v1(app)
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    start_service()
