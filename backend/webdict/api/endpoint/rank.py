from typing import Dict, Iterable, List
from functools import cmp_to_key
import random

from fastapi import FastAPI
from asgiref.sync import sync_to_async
from webdict.api.comparator.comparator import make_top_word_comparator
from webdict.api.database.database import find_dictionary_by_code, find_user_by_id
from webdict.api.dto.rank import RankModel
from webdict.api.endpoint.dictionary import is_dictionary_reversed

from webdict.djangoapp.words import models
from webdict.djangoapp.words.time import datetime_to_str


def setup_rank_endpoints(app: FastAPI):
    @app.get("/rank/all/{user_id}/{dict_code}")
    async def rank_all_user_dict(user_id: str, dict_code: str) -> List[RankModel]:
        return await _list_all_ranks(user_id, dict_code)

    @app.get("/rank/top/{user_id}/{dict_code}")
    async def rank_top_user_dict(user_id: str, dict_code: str) -> RankModel:
        return await _get_top_rank(user_id, dict_code)


@sync_to_async
def _list_all_ranks(user_id: str, dict_code: str) -> List[RankModel]:
    user = find_user_by_id(user_id)
    dictionary = find_dictionary_by_code(dict_code)
    reversed = is_dictionary_reversed(dict_code)

    rank_models = list(_generate_all_ranks(user, dictionary, reversed))
    counter_ranks = list(_generate_all_ranks(user, dictionary, not reversed))
    ranks = _combine_counter_ranks(rank_models, counter_ranks)

    sorted_ranks = sorted(ranks, key=cmp_to_key(make_top_word_comparator()))
    return [_cleanup_rank_model(rank) for rank in sorted_ranks]


def _generate_all_ranks(
    user: models.User, dictionary: models.Dictionary, reversed: bool
) -> Iterable[models.Rank]:
    objects = models.Rank.objects.filter(
        reversed_dictionary=reversed,
        user_word__user=user,
        user_word__word__dictionary=dictionary,
    )
    for model in objects:
        yield model


def rank_model_to_dto(model: models.Rank) -> RankModel:
    return RankModel(
        rankId=model.id,
        dictionaryId=model.user_word.word.dictionary.id,
        reversedDictionary=model.reversed_dictionary,
        wordName=model.user_word.word.name,
        definition=model.user_word.word.definition,
        rankValue=model.rank_value,
        triesCount=model.tries_count,
        lastUse=datetime_to_str(model.last_use) if model.last_use else None,
        counter_rank=None,
        last_use_datetime=model.last_use,
    )


def _cleanup_rank_model(model: RankModel) -> RankModel:
    model.counter_rank = None
    model.last_use_datetime = None
    return model


@sync_to_async
def _get_top_rank(user_id: str, dict_code: str) -> RankModel:
    user = find_user_by_id(user_id)
    dictionary = find_dictionary_by_code(dict_code)
    reversed = is_dictionary_reversed(dict_code)

    rank_models = list(_generate_all_ranks(user, dictionary, reversed))
    counter_ranks = list(_generate_all_ranks(user, dictionary, not reversed))
    ranks = _combine_counter_ranks(rank_models, counter_ranks)

    random.shuffle(ranks)
    sorted_ranks = sorted(ranks, key=cmp_to_key(make_top_word_comparator()))
    rank = sorted_ranks[0]

    return _cleanup_rank_model(rank)


def _combine_counter_ranks(ranks: List[models.Rank], counter_ranks: List[models.Rank]) -> List[RankModel]:
    counter_rank_ids = {rank.user_word.id: rank for rank in counter_ranks}
    out_ranks = []

    for rank_model in ranks:
        rank = rank_model_to_dto(rank_model)

        word_id = rank_model.user_word.id
        if word_id in counter_rank_ids:
            counter_rank_model = counter_rank_ids[word_id]
            rank.counter_rank = rank_model_to_dto(rank_model)

        out_ranks.append(rank)

    return out_ranks
