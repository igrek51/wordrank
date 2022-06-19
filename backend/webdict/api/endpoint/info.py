from fastapi import FastAPI


def setup_info_endpoints(app: FastAPI):
    @app.get("/info")
    async def info():
        return {
            "environmentName": "WordRank",
            "buildVersion": "2.1.0",
            "status": "UP",
        }
