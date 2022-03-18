from typing import Dict, Iterable, List
from functools import cmp_to_key

from fastapi import FastAPI
from asgiref.sync import sync_to_async
from webdict.api.comparator import make_top_word_comparator
from webdict.api.database import find_dictionary_by_code, find_user_by_id
from webdict.api.dictionary import is_dictionary_reversed

from webdict.djangoapp.words import models
from webdict.djangoapp.words.time import datetime_to_str


def setup_rank_endpoints(app: FastAPI):
    @app.get("/rank/all/{user_id}/{dict_code}")
    async def rank_all_user_dict(user_id: str, dict_code: str):
        return await _list_all_ranks(user_id, dict_code)


@sync_to_async
def _list_all_ranks(user_id: str, dict_code: str) -> List[Dict]:
    user = find_user_by_id(user_id)
    dictionary = find_dictionary_by_code(dict_code)
    reversed = is_dictionary_reversed(dict_code)
    ranks = list(_generate_all_ranks(user, dictionary, reversed))
    sorted_ranks = sorted(ranks, key=cmp_to_key(make_top_word_comparator()))
    return [rank_model_to_dto(rank) for rank in sorted_ranks]


def _generate_all_ranks(user: models.User, dictionary: models.Dictionary, reversed: bool) -> Iterable[Dict]:
    objects = models.Rank.objects.filter(
        reversed_dictionary=reversed, 
        user_word__user=user, 
        user_word__word__dictionary=dictionary,
    )
    for model in objects:
        yield model


def rank_model_to_dto(model: models.Rank) -> Dict:
    return {
        "rankId": model.id,
        "dictionaryId": model.user_word.word.dictionary.id,
        "reversedDictionary": model.reversed_dictionary,
        "wordName": model.user_word.word.name,
        "definition": model.user_word.word.definition,
        "rankValue": model.rank_value,
        "triesCount": model.tries_count,
        "lastUse": datetime_to_str(model.last_use),
    }
