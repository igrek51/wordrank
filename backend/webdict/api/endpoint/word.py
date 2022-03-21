from typing import Tuple

from fastapi import FastAPI
from pydantic import BaseModel
from asgiref.sync import sync_to_async

from webdict.api.database.database import find_dictionary_by_code, find_user_by_id, word_exists
from webdict.api.endpoint.dictionary import is_dictionary_reversed
from webdict.api.dto.payload import PayloadResponse
from webdict.djangoapp.words import models
from webdict.api.logs import get_logger
from webdict.djangoapp.words.time import now

logger = get_logger()


class Word(BaseModel):
    word: str
    definition: str
    dictionaryCode: str
    userId: str


def setup_word_endpoints(app: FastAPI):
    @app.post("/word")
    async def add_word(word: Word) -> PayloadResponse:
        return await _add_word(word)


@sync_to_async
def _add_word(word: Word) -> PayloadResponse:
    try:
        response, message = _must_add_word(word)
        return PayloadResponse(payload=response, message=message)
    except BaseException as e:
        return PayloadResponse(
            payload=None,
            httpStatus=400,
            message=str(e),
        )


def _must_add_word(word: Word) -> Tuple[Word, str]:
    user: models.User = find_user_by_id(word.userId)
    dictionary: models.Dictionary = find_dictionary_by_code(word.dictionaryCode)

    if not word.word:
        raise ValueError("word name was not given")
    if not word.definition:
        raise ValueError("word definition was not given")

    if word_exists(word.word, user.id, dictionary):
        raise ValueError("word already exists")

    word_model = models.Word(
        dictionary=dictionary,
        name=word.word,
        definition=word.definition,
        create_time=now(),
    )
    word_model.save()

    user_word = models.UserWord(
        user=user,
        word=word_model,
    )
    user_word.save()

    rank1 = models.Rank(
        reversed_dictionary=False,
        rank_value=0,
        user_word=user_word,
    )
    rank1.save()
    rank2 = models.Rank(
        reversed_dictionary=True,
        rank_value=0,
        user_word=user_word,
    )
    rank2.save()

    logger.info(f'new word has been added: {word.word} - {word.definition}')
    return word, f'Word "{word.word} - {word.definition}" has been added successfuly'
