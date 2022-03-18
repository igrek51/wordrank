from termios import VT1
from webdict.api.dto.rank import RankModel
from webdict.djangoapp.words.time import datetime_to_timestamp, now, seconds_ago


COOLDOWN_SECONDS = 30 * 60
COOLDOWN_MAX_PENALTY = 60 * 60 * 24 * 365


def make_oldest_word_comparator():
    value_cache = {}
    now_dt = now()

    def get_single_cooldown_penalty(rank: RankModel) -> float:
        if rank.last_use_datetime is None:
            return 0

        elapsed_seconds = seconds_ago(rank.last_use_datetime)
        
        if elapsed_seconds >= COOLDOWN_SECONDS:
            return 0
        
        return (COOLDOWN_SECONDS - elapsed_seconds) * COOLDOWN_MAX_PENALTY / COOLDOWN_SECONDS
    
    def get_both_cooldown_penalty(rank: RankModel) -> float:
        penalty = get_single_cooldown_penalty(rank)
        if rank.counter_rank is not None:
            return penalty
        counter_penalty = get_single_cooldown_penalty(rank.counter_rank)
        return max(penalty, counter_penalty)

    def get_effective_value(rank: RankModel) -> float:
        last_use = rank.last_use_datetime
        if last_use is None:
            return datetime_to_timestamp(now_dt)
        epoch_seconds = datetime_to_timestamp(last_use)
        return epoch_seconds + get_both_cooldown_penalty(rank)

    def get_cached_value(rank: RankModel):
        cached = value_cache.get(rank.rankId)
        if cached is not None:
            return cached
        value = get_effective_value(rank)
        value_cache[rank.rankId] = value
        return value

    def compare(r1: RankModel, r2: RankModel) -> float:
        v1 = get_cached_value(r1)
        v2 = get_cached_value(r2)
        return v1 - v2

    return compare
