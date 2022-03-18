from typing import Dict, Iterable, List
from functools import cmp_to_key

from fastapi import FastAPI
from asgiref.sync import sync_to_async

from webdict.api.comparator.top import make_top_word_comparator
from webdict.api.database.database import find_dictionary_by_code, find_user_by_id
from webdict.api.dto.stats import StatisticsModel
from webdict.api.endpoint.dictionary import is_dictionary_reversed
from webdict.djangoapp.words import models
from webdict.djangoapp.words.time import datetime_to_str, now
from webdict.api.logs import get_logger

logger = get_logger()


def setup_stats_endpoints(app: FastAPI):
    @app.get("/stats/{user_id}/{dict_code}")
    async def stats_user_dict(user_id: str, dict_code: str) -> List[StatisticsModel]:
        return await _list_stats(user_id, dict_code)


@sync_to_async
def _list_stats(user_id: str, dict_code: str) -> List[StatisticsModel]:
    user = find_user_by_id(user_id)
    dictionary = find_dictionary_by_code(dict_code)
    reversed = is_dictionary_reversed(dict_code)

    return []
