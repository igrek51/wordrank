from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse


def creat_fastapi_app() -> FastAPI:
    app = FastAPI()

    subapi = FastAPI()
    setup_api_endpoints(subapi)
    app.mount("/webdict/api", subapi)
    app.mount("/webdict///api", subapi)

    @app.get("/")
    @app.get("/webdict")
    @app.get("/webdict/")
    async def home():
        return RedirectResponse("/webdict/index.html")

    app.mount("/webdict", StaticFiles(directory="static"), name="webdict_static")

    return app


def setup_api_endpoints(app: FastAPI):
    @app.get("/info")
    async def info():
        return {
            "environmentName": "WebDict",
            "buildVersion": "2.0.1",
            "status": "UP",
        }
