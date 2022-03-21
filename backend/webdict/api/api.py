from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from webdict.api.endpoint.dictionary import setup_dictionary_endpoints
from webdict.api.endpoint.info import setup_info_endpoints
from webdict.api.endpoint.rank import setup_rank_endpoints
from webdict.api.endpoint.user import setup_user_endpoints
from webdict.api.endpoint.word import setup_word_endpoints
from webdict.api.endpoint.stats import setup_stats_endpoints
from webdict.api.errors import AuthError
from webdict.api.logs import get_logger

logger = get_logger()


def creat_fastapi_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

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

    @subapi.exception_handler(AuthError)
    async def auth_error_handler(request: Request, exc: AuthError):
        message = f"Unauthorized: {exc}"
        logger.error(message)
        return JSONResponse(
            status_code=401,
            content={
                'error': message,
            },
        )

    return app


def setup_api_endpoints(app: FastAPI):
    setup_info_endpoints(app)
    setup_rank_endpoints(app)
    setup_user_endpoints(app)
    setup_dictionary_endpoints(app)
    setup_word_endpoints(app)
    setup_stats_endpoints(app)
