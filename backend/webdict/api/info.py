from fastapi import FastAPI


def setup_info_endpoints(app: FastAPI):
    @app.get("/info")
    async def info():
        return {
            "environmentName": "WebDict",
            "buildVersion": "2.0.1",
            "status": "UP",
        }
