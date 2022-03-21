from typing import Dict, Iterable, List

from fastapi import FastAPI, Cookie
from asgiref.sync import sync_to_async

from webdict.djangoapp.words import models
from webdict.api.session import verify_session


def setup_user_endpoints(app: FastAPI):
    @app.get("/user")
    async def users(sessionid: str = Cookie(None)):
        await verify_session(sessionid)
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
