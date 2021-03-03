from fastapi import FastAPI
import uvicorn

from webdict.djangoapp.app.asgi import application as django_app
from webdict.api.dispatcher import AsgiDispatcher

fastapi_app = FastAPI()

@fastapi_app.get("/")
async def root():
    return {"status": "pass"}


if __name__ == '__main__':
    dispatcher = AsgiDispatcher({
        '/admin': django_app,
        '/static/admin': django_app,
    }, default=fastapi_app)

    uvicorn.run(app=dispatcher)