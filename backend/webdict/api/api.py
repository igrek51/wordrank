import fastapi
from fastapi import FastAPI


def creat_fastapi_app() -> FastAPI:
    fastapi_app = FastAPI()

    @fastapi_app.get("/")
    async def root():
        return {"status": "ok"}

    return fastapi_app
