from typing import Dict, Iterable, List

from fastapi import FastAPI
from asgiref.sync import sync_to_async

from webdict.djangoapp.words import models


def setup_dictionary_endpoints(app: FastAPI):
    @app.get("/dictionary")
    async def dictionaries():
        return await _list_dictionaries()


@sync_to_async
def _list_dictionaries() -> List[Dict]:
    return list(_generate_dictionaries())


def _generate_dictionaries() -> Iterable[Dict]:
    objects = models.Dictionary.objects.all()
    for object in objects:
        yield {
            "dictionaryId": object.id,
            "sourceLanguage": object.source_language.code,
            "targetLanguage": object.target_language.code,
        }