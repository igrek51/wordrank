from typing import Dict, Iterable, List

from fastapi import FastAPI
from asgiref.sync import sync_to_async

from webdict.djangoapp.words import models


def setup_user_endpoints(app: FastAPI):
    @app.get("/user")
    async def users():
        return await _list_users()


@sync_to_async
def _list_users() -> List[Dict]:
    return list(_generate_users())


def _generate_users() -> Iterable[Dict]:
    objects = models.User.objects.all().order_by('login')
    for object in objects:
        yield {
            "id": object.id,
            "login": object.login,
        }
