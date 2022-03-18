from typing import Dict, Iterable
from fastapi import FastAPI

from asgiref.sync import sync_to_async

from webdict.djangoapp.words import models


def setup_user_endpoints(app: FastAPI):
    @app.get("/user")
    async def info():
        return [u async for u in _list_users()]


async def _list_users() -> Iterable[Dict]:
    objects = await _get_all_users()
    for object in objects:
        yield {
            "id": object.id,
            "login": object.login,
        }


@sync_to_async
def _get_all_users():
    return list(models.User.objects.all().order_by('login'))
