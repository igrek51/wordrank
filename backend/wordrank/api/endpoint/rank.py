from typing import List
from functools import cmp_to_key
import random

from fastapi import FastAPI, Cookie
from asgiref.sync import sync_to_async

from wordrank.api.comparator.hardest import make_hardest_word_comparator
from wordrank.api.comparator.latest import make_latest_word_comparator
from wordrank.api.comparator.oldest import make_oldest_word_comparator
from wordrank.api.comparator.top import make_top_word_comparator
from wordrank.api.database.database import find_dictionary_by_code, find_rank_by_id, find_user_by_id, generate_all_ranks, generate_all_userwords, generate_all_words
from wordrank.api.dto.payload import PayloadResponse
from wordrank.api.dto.rank import InternalRank, ExternalRank
from wordrank.api.endpoint.dictionary import is_dictionary_reversed
from wordrank.djangoapp.words import models
from wordrank.djangoapp.words.time import datetime_to_str, now
from wordrank.api.metrics import metric_good_answers, metric_bad_answers, metric_all_answers
from wordrank.api.logs import get_logger
from wordrank.api.session import verify_session

logger = get_logger()


def setup_rank_endpoints(app: FastAPI):
    @app.get("/rank/all/{user_id}/{dict_code}")
    async def rank_all_user_dict(user_id: str, dict_code: str, sessionid: str = Cookie(None)) -> List[ExternalRank]:
        await verify_session(sessionid)
        return await _list_all_ranks(user_id, dict_code)

    @app.get("/rank/top/{user_id}/{dict_code}")
    async def rank_top_user_dict(user_id: str, dict_code: str, sessionid: str = Cookie(None)) -> ExternalRank:
        await verify_session(sessionid)
        return await _get_top_rank(user_id, dict_code)

    @app.get("/rank/hardest/{user_id}/{dict_code}")
    async def rank_hardest_user_dict(user_id: str, dict_code: str, sessionid: str = Cookie(None)) -> ExternalRank:
        await verify_session(sessionid)
        return await _get_hardest_rank(user_id, dict_code)

    @app.get("/rank/oldest/{user_id}/{dict_code}")
    async def rank_oldest_user_dict(user_id: str, dict_code: str, sessionid: str = Cookie(None)) -> ExternalRank:
        await verify_session(sessionid)
        return await _get_oldest_rank(user_id, dict_code)

    @app.get("/rank/latest/{user_id}/{dict_code}")
    async def rank_latest_user_dict(user_id: str, dict_code: str, sessionid: str = Cookie(None)) -> ExternalRank:
        await verify_session(sessionid)
        return await _get_latest_rank(user_id, dict_code)

    @app.post("/rank/{rank_id}/skip")
    async def rank_id_skip(rank_id: str, sessionid: str = Cookie(None)) -> PayloadResponse:
        await verify_session(sessionid)
        metric_all_answers.inc()
        return await _update_rank_realively(rank_id, 0)

    @app.post("/rank/{rank_id}/answer/correct")
    async def rank_id_correct(rank_id: str, sessionid: str = Cookie(None)) -> PayloadResponse:
        await verify_session(sessionid)
        metric_good_answers.inc()
        metric_all_answers.inc()
        return await _update_rank_realively(rank_id, -1)

    @app.post("/rank/{rank_id}/answer/wrong")
    async def rank_id_wrong(rank_id: str, sessionid: str = Cookie(None)) -> PayloadResponse:
        await verify_session(sessionid)
        metric_bad_answers.inc()
        metric_all_answers.inc()
        return await _update_rank_realively(rank_id, +1)

    @app.get("/rank/offset/{user_id}/{dict_code}/{offset}")
    async def rank_move_by_offset(user_id: str, dict_code: str, offset: float, sessionid: str = Cookie(None)):
        await verify_session(sessionid)
        return await _move_ranks_by_offset(user_id, dict_code, offset)


@sync_to_async
def _list_all_ranks(user_id: str, dict_code: str) -> List[ExternalRank]:
    user = find_user_by_id(user_id)
    dictionary = find_dictionary_by_code(dict_code)
    reversed = is_dictionary_reversed(dict_code)

    rank_models = list(generate_all_ranks(user, dictionary, reversed))
    counter_ranks = list(generate_all_ranks(user, dictionary, not reversed))
    internal_ranks: List[InternalRank] = combine_counter_ranks(rank_models, counter_ranks)

    sorted_ranks: List[InternalRank] = sorted(internal_ranks, key=cmp_to_key(make_top_word_comparator()))
    return internal_ranks_to_external(sorted_ranks, dictionary.id, reversed, user)


@sync_to_async
def _get_top_rank(user_id: str, dict_code: str) -> ExternalRank:
    comparator = make_top_word_comparator()
    return _get_next_rank(user_id, dict_code, comparator)


@sync_to_async
def _get_hardest_rank(user_id: str, dict_code: str) -> ExternalRank:
    comparator = make_hardest_word_comparator()
    return _get_next_rank(user_id, dict_code, comparator)


@sync_to_async
def _get_oldest_rank(user_id: str, dict_code: str) -> ExternalRank:
    comparator = make_oldest_word_comparator()
    return _get_next_rank(user_id, dict_code, comparator)


@sync_to_async
def _get_latest_rank(user_id: str, dict_code: str) -> ExternalRank:
    comparator = make_latest_word_comparator()
    return _get_next_rank(user_id, dict_code, comparator)


def _get_next_rank(user_id: str, dict_code: str, comparator) -> ExternalRank:
    user = find_user_by_id(user_id)
    dictionary = find_dictionary_by_code(dict_code)
    reversed = is_dictionary_reversed(dict_code)

    rank_models = list(generate_all_ranks(user, dictionary, reversed))
    counter_ranks = list(generate_all_ranks(user, dictionary, not reversed))

    internal_ranks: List[InternalRank] = combine_counter_ranks(rank_models, counter_ranks)

    random.shuffle(internal_ranks)
    sorted_ranks = sorted(internal_ranks, key=cmp_to_key(comparator))

    if len(sorted_ranks) == 0:
        return None
    internal_rank = sorted_ranks[0]
    rank_model = find_rank_by_id(internal_rank.rankId)

    return rank_model_to_external(rank_model)


def combine_counter_ranks(
    ranks: List[models.Rank], 
    counter_ranks: List[models.Rank],
) -> List[InternalRank]:
    counter_rank_ids = {rank.user_word_id: rank for rank in counter_ranks}
    out_ranks = []

    for rank_model in ranks:
        rank = rank_model_to_internal(rank_model)

        word_id = rank_model.user_word_id
        if word_id in counter_rank_ids:
            counter_rank_model = counter_rank_ids[word_id]
            rank.counter_rank = rank_model_to_internal(counter_rank_model)

        out_ranks.append(rank)

    return out_ranks


def rank_model_to_internal(
    model: models.Rank,
) -> InternalRank:
    last_use = model.last_use
    return InternalRank(
        rankId=model.id,
        rankValue=float(model.rank_value),
        triesCount=model.tries_count,
        lastUse=datetime_to_str(last_use) if last_use else None,
        counter_rank=None,
        last_use_datetime=last_use,
        user_word_id=model.user_word_id,
    )


def rank_model_to_external(model: models.Rank) -> ExternalRank:
    last_use = model.last_use
    return ExternalRank(
        rankId=model.id,
        dictionaryId=model.user_word.word.dictionary.id,
        reversedDictionary=model.reversed_dictionary,
        wordName=model.user_word.word.name,
        definition=model.user_word.word.definition,
        rankValue=float(model.rank_value),
        triesCount=model.tries_count,
        lastUse=datetime_to_str(last_use) if last_use else None,
    )


def internal_ranks_to_external(
    ranks: List[InternalRank],
    dictionary_id: str, 
    reversed_dictionary: bool,
    user: models.User,
) -> List[ExternalRank]:
    wordnames = {}
    word_models = generate_all_words(dictionary_id)
    for word_model in word_models:
        wordnames[word_model.id] = (word_model.name, word_model.definition)

    userwordnames = {}
    userword_models = generate_all_userwords(user, dictionary_id)
    for userword in userword_models:
        userwordnames[userword.id] = wordnames[userword.word_id]

    ext_ranks = []
    for rank in ranks:
        word_name = userwordnames[rank.user_word_id][0]
        definition = userwordnames[rank.user_word_id][1]
        ext_rank = ExternalRank(
            rankId=rank.rankId,
            dictionaryId=dictionary_id,
            reversedDictionary=reversed_dictionary,
            wordName=word_name,
            definition=definition,
            rankValue=rank.rankValue,
            triesCount=rank.triesCount,
            lastUse=rank.lastUse,
        )
        ext_ranks.append(ext_rank)
    return ext_ranks


@sync_to_async
def _update_rank_realively(
    rank_id: str, 
    rank_increase: float,
) -> PayloadResponse:
    rank = find_rank_by_id(rank_id)
    rank.rank_value = float(rank.rank_value) + rank_increase
    rank.tries_count += 1
    rank.last_use = now()
    rank.save()

    return PayloadResponse(
        payload=rank_model_to_external(rank),
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
