import uvicorn

from webdict.djangoapp.app.asgi import application as django_app
from webdict.api.api import creat_fastapi_app
from webdict.api.dispatcher import AsgiDispatcher


def main():
    fastapi_app = creat_fastapi_app()
    dispatcher = AsgiDispatcher({
        '/admin': django_app,
        '/static/admin': django_app,
    }, default=fastapi_app)

    uvicorn.run(app=dispatcher)

if __name__ == '__main__':
    main()
