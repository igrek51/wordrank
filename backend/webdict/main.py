import uvicorn
from prometheus_client import make_asgi_app

from wordrank.djangoapp.app.asgi import application as django_app
from wordrank.api.api import creat_fastapi_app
from wordrank.api.dispatcher import AsgiDispatcher
from wordrank.api.logs import get_logger, configure_logs

logger = get_logger()


def main():
    configure_logs(log_level='debug')
    logger = get_logger()
    logger.info("Starting HTTP server...")

    fastapi_app = creat_fastapi_app()
    metrics_app = make_asgi_app()

    dispatcher = AsgiDispatcher({
        '/admin': django_app,
        '/static/admin': django_app,
        '/dump': django_app,
        '/metrics': metrics_app,
    }, default=fastapi_app)

    uvicorn.run(app=dispatcher, host="0.0.0.0", port=8000, log_level="debug")

if __name__ == '__main__':
    main()
