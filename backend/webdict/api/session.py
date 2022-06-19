from typing import Optional

from asgiref.sync import sync_to_async
from django.contrib.auth import SESSION_KEY
from django.contrib.sessions.models import Session

from wordrank.api.errors import AuthError


@sync_to_async
def verify_session(sessionid: Optional[str]):
    if not sessionid:
        raise AuthError('Empty session ID')
    try:
        session = Session.objects.get(session_key=sessionid)
        session.get_decoded()[SESSION_KEY]
    except (Session.DoesNotExist, KeyError):
        raise AuthError('Invalid session ID')
