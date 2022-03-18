from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from webdict.api.endpoint.dictionary import setup_dictionary_endpoints
from webdict.api.endpoint.info import setup_info_endpoints
from webdict.api.endpoint.rank import setup_rank_endpoints
from webdict.api.endpoint.user import setup_user_endpoints
from webdict.api.endpoint.word import setup_word_endpoints


def creat_fastapi_app() -> FastAPI:
    app = FastAPI()

    subapi = FastAPI()
    setup_api_endpoints(subapi)
    app.mount("/webdict/api", subapi)
    app.mount("/webdict//api", subapi)
    app.mount("/webdict///api", subapi)

    @app.get("/")
    @app.get("/webdict")
    @app.get("/webdict/")
    async def home():
        return RedirectResponse("/webdict/index.html")

    app.mount("/webdict", StaticFiles(directory="static"), name="webdict_static")

    return app


def setup_api_endpoints(app: FastAPI):
    setup_info_endpoints(app)
    setup_rank_endpoints(app)
    setup_user_endpoints(app)
    setup_dictionary_endpoints(app)
    setup_word_endpoints(app)
