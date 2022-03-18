from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse


def creat_fastapi_app() -> FastAPI:
    app = FastAPI()

    @app.get("/")
    @app.get("/webdict")
    @app.get("/webdict/")
    async def root():
        return RedirectResponse('/webdict/index.html')

    app.mount('/webdict', StaticFiles(directory="static"), name="webdict_static")

    return app
