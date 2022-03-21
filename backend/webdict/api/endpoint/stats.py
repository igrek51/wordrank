from typing import Callable, Dict, Iterable, List
from functools import cmp_to_key

from fastapi import FastAPI
from asgiref.sync import sync_to_async

from webdict.api.comparator.top import get_single_cooldown_penalty, make_top_word_comparator
from webdict.api.database.database import find_dictionary_by_code, find_user_by_id, generate_all_ranks
from webdict.api.dto.rank import RankModel
from webdict.api.dto.stats import ProgressBarData, StatisticsModel
from webdict.api.endpoint.dictionary import is_dictionary_reversed
from webdict.api.endpoint.rank import combine_counter_ranks, rank_model_to_dto
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

    straight_ranks = list(generate_all_ranks(user, dictionary, False))
    reversed_ranks = list(generate_all_ranks(user, dictionary, True))

    dict_stats: List[StatisticsModel] = [
        _generate_dict_stats(dictionary, False, straight_ranks), 
        _generate_dict_stats(dictionary, True, reversed_ranks), 
        _generate_both_direction_stats(dictionary, straight_ranks, reversed_ranks), 
    ]

    return dict_stats


def _generate_dict_stats(
    dictionary: models.Dictionary, 
    reversed: bool, 
    ranks: List[models.Rank],
) -> StatisticsModel:
    dict_display_name = _dictionary_display_name(dictionary, reversed)
    all_count = len(ranks)

    rank_models: List[RankModel] = [rank_model_to_dto(rank) for rank in ranks]

    trained_count = _count_ranks(rank_models, _is_rank_model_trained)
    training_in_progress_count = _count_ranks(rank_models, _is_rank_model_in_progress)
    touched_count = _count_ranks(rank_models, _is_rank_model_touched)
    cooling_down_count = _count_ranks(rank_models, _is_rank_model_cooling_down)
    rankSum = sum([rank.rankValue for rank in rank_models])

    return StatisticsModel(
        dictDisplayName=dict_display_name,
        allCount=all_count,
        trained=_make_progress_bar_data(trained_count, all_count),
        trainingInProgress=_make_progress_bar_data(training_in_progress_count, all_count),
        touched=_make_progress_bar_data(touched_count, all_count),
        coolingDown=_make_progress_bar_data(cooling_down_count, all_count),
        rankSum=rankSum,
    )


def _generate_both_direction_stats(
    dictionary: models.Dictionary, 
    straight_ranks: List[models.Rank],
    reversed_ranks: List[models.Rank],
) -> StatisticsModel:
    dict_display_name = f'{dictionary.source_language} <-> {dictionary.target_language} (both directions)'
    ranks: List[RankModel] = combine_counter_ranks(straight_ranks, reversed_ranks)
    all_count = len(ranks)

    trained_count = _count_ranks(ranks, _predicate_both_ranks(_is_rank_model_trained))
    training_in_progress_count = _count_ranks(ranks, _predicate_both_ranks(_is_rank_model_in_progress))
    touched_count = _count_ranks(ranks, _predicate_both_ranks(_is_rank_model_touched))
    cooling_down_count = _count_ranks(ranks, _predicate_both_ranks(_is_rank_model_cooling_down))
    straight_rank_sum = sum([rank.rankValue for rank in ranks])
    reversed_rank_sum = sum([rank.counter_rank.rankValue for rank in ranks])

    return StatisticsModel(
        dictDisplayName=dict_display_name,
        allCount=all_count,
        trained=_make_progress_bar_data(trained_count, all_count),
        trainingInProgress=_make_progress_bar_data(training_in_progress_count, all_count),
        touched=_make_progress_bar_data(touched_count, all_count),
        coolingDown=_make_progress_bar_data(cooling_down_count, all_count),
        rankSum=straight_rank_sum + reversed_rank_sum,
    )


def _count_ranks(ranks: List[RankModel], predicate: Callable[[RankModel], bool]) -> int:
    return sum([1 for rank in ranks if predicate(rank)])


def _predicate_both_ranks(single_predicate: Callable[[RankModel], bool]) -> Callable[[RankModel], bool]:
    def predicate(rank: RankModel) -> bool:
        return single_predicate(rank) and single_predicate(rank.counter_rank)
    return predicate


def _dictionary_display_name(dictionary: models.Dictionary, reversed: bool) -> str:
    if reversed:
        return f'{dictionary.source_language} <- {dictionary.target_language}'
    else:
        return f'{dictionary.source_language} -> {dictionary.target_language}'


def _make_progress_bar_data(count: int, all_count: int) -> ProgressBarData:
    percentage = count * 100 / all_count
    percentage_str = f'{percentage:.2f}'
    return ProgressBarData(
        count=count,
        percentage=percentage_str,
    )


def _is_rank_model_trained(rank: RankModel) -> bool:
    return rank.rankValue < 0 and rank.triesCount > 0


def _is_rank_model_in_progress(rank: RankModel) -> bool:
    return rank.rankValue >= 0 and rank.triesCount > 0


def _is_rank_model_touched(rank: RankModel) -> bool:
    return rank.triesCount > 0


def _is_rank_model_cooling_down(rank: RankModel) -> bool:
    return get_single_cooldown_penalty(rank) > 0