from typing import Dict, Iterable, List
from functools import cmp_to_key
import random

from fastapi import FastAPI
from asgiref.sync import sync_to_async
from webdict.api.comparator.hardest import make_hardest_word_comparator
from webdict.api.comparator.latest import make_latest_word_comparator
from webdict.api.comparator.oldest import make_oldest_word_comparator

from webdict.api.comparator.top import make_top_word_comparator
from webdict.api.database.database import find_dictionary_by_code, find_rank_by_id, find_user_by_id, generate_all_ranks
from webdict.api.dto.payload import PayloadResponse
from webdict.api.dto.rank import RankModel
from webdict.api.endpoint.dictionary import is_dictionary_reversed
from webdict.djangoapp.words import models
from webdict.djangoapp.words.time import datetime_to_str, now
from webdict.api.logs import get_logger

logger = get_logger()


def setup_rank_endpoints(app: FastAPI):
    @app.get("/rank/all/{user_id}/{dict_code}")
    async def rank_all_user_dict(user_id: str, dict_code: str) -> List[RankModel]:
        return await _list_all_ranks(user_id, dict_code)

    @app.get("/rank/top/{user_id}/{dict_code}")
    async def rank_top_user_dict(user_id: str, dict_code: str) -> RankModel:
        return await _get_top_rank(user_id, dict_code)

    @app.get("/rank/hardest/{user_id}/{dict_code}")
    async def rank_hardest_user_dict(user_id: str, dict_code: str) -> RankModel:
        return await _get_hardest_rank(user_id, dict_code)

    @app.get("/rank/oldest/{user_id}/{dict_code}")
    async def rank_oldest_user_dict(user_id: str, dict_code: str) -> RankModel:
        return await _get_oldest_rank(user_id, dict_code)

    @app.get("/rank/latest/{user_id}/{dict_code}")
    async def rank_latest_user_dict(user_id: str, dict_code: str) -> RankModel:
        return await _get_latest_rank(user_id, dict_code)

    @app.post("/rank/{rank_id}/skip")
    async def rank_id_skip(rank_id: str) -> PayloadResponse:
        return await _update_rank_realively(rank_id, 0)

    @app.post("/rank/{rank_id}/answer/correct")
    async def rank_id_correct(rank_id: str) -> PayloadResponse:
        return await _update_rank_realively(rank_id, -1)

    @app.post("/rank/{rank_id}/answer/wrong")
    async def rank_id_wrong(rank_id: str) -> PayloadResponse:
        return await _update_rank_realively(rank_id, +1)

    @app.get("/rank/offset/{user_id}/{dict_code}/{offset}")
    async def rank_move_by_offset(user_id: str, dict_code: str, offset: float):
        return await _move_ranks_by_offset(user_id, dict_code, offset)


@sync_to_async
def _list_all_ranks(user_id: str, dict_code: str) -> List[RankModel]:
    user = find_user_by_id(user_id)
    dictionary = find_dictionary_by_code(dict_code)
    reversed = is_dictionary_reversed(dict_code)

    rank_models = list(generate_all_ranks(user, dictionary, reversed))
    counter_ranks = list(generate_all_ranks(user, dictionary, not reversed))
    ranks = combine_counter_ranks(rank_models, counter_ranks)

    sorted_ranks = sorted(ranks, key=cmp_to_key(make_top_word_comparator()))
    return [_cleanup_rank_model(rank) for rank in sorted_ranks]


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
    comparator = make_top_word_comparator()
    return _get_next_rank(user_id, dict_code, comparator)


@sync_to_async
def _get_hardest_rank(user_id: str, dict_code: str) -> RankModel:
    comparator = make_hardest_word_comparator()
    return _get_next_rank(user_id, dict_code, comparator)


@sync_to_async
def _get_oldest_rank(user_id: str, dict_code: str) -> RankModel:
    comparator = make_oldest_word_comparator()
    return _get_next_rank(user_id, dict_code, comparator)


@sync_to_async
def _get_latest_rank(user_id: str, dict_code: str) -> RankModel:
    comparator = make_latest_word_comparator()
    return _get_next_rank(user_id, dict_code, comparator)


def _get_next_rank(user_id: str, dict_code: str, comparator) -> RankModel:
    user = find_user_by_id(user_id)
    dictionary = find_dictionary_by_code(dict_code)
    reversed = is_dictionary_reversed(dict_code)

    rank_models = list(generate_all_ranks(user, dictionary, reversed))
    counter_ranks = list(generate_all_ranks(user, dictionary, not reversed))
    ranks = combine_counter_ranks(rank_models, counter_ranks)

    random.shuffle(ranks)
    sorted_ranks = sorted(ranks, key=cmp_to_key(comparator))
    if len(sorted_ranks) == 0:
        return None
    rank = sorted_ranks[0]

    return _cleanup_rank_model(rank)


def combine_counter_ranks(ranks: List[models.Rank], counter_ranks: List[models.Rank]) -> List[RankModel]:
    counter_rank_ids = {rank.user_word.id: rank for rank in counter_ranks}
    out_ranks = []

    for rank_model in ranks:
        rank = rank_model_to_dto(rank_model)

        word_id = rank_model.user_word.id
        if word_id in counter_rank_ids:
            counter_rank_model = counter_rank_ids[word_id]
            rank.counter_rank = rank_model_to_dto(counter_rank_model)

        out_ranks.append(rank)

    return out_ranks


@sync_to_async
def _update_rank_realively(rank_id: str, rank_increase: float) -> PayloadResponse:
    rank = find_rank_by_id(rank_id)
    rank.rank_value = float(rank.rank_value) + rank_increase
    rank.tries_count += 1
    rank.last_use = now()
    rank.save()

    return PayloadResponse(
        payload=rank_model_to_dto(rank),
    )


@sync_to_async
def _move_ranks_by_offset(user_id: str, dict_code: str, offset: float):
    user = find_user_by_id(user_id)
    dictionary = find_dictionary_by_code(dict_code)
    reversed = is_dictionary_reversed(dict_code)

    objects = models.Rank.objects.filter(
        reversed_dictionary=reversed,
        user_word__user=user,
        user_word__word__dictionary=dictionary,
    )
    for model in objects:
        model.rank_value = float(model.rank_value) + offset
        model.save()

    logger.info(f"All ranks moved by offset {offset} for user {user.login} and dict {dict_code}")
