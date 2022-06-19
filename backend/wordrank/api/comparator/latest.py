from wordrank.api.dto.rank import InternalRank
from wordrank.djangoapp.words.time import datetime_to_timestamp, now, seconds_ago


COOLDOWN_SECONDS = 30 * 60
COOLDOWN_MAX_PENALTY = 60 * 60 * 24 * 365


def make_latest_word_comparator():
    value_cache = {}
    now_dt = now()

    def get_single_cooldown_penalty(rank: InternalRank) -> float:
        if rank.last_use_datetime is None:
            return 0

        elapsed_seconds = seconds_ago(rank.last_use_datetime)
        
        if elapsed_seconds >= COOLDOWN_SECONDS:
            return 0
        
        return (COOLDOWN_SECONDS - elapsed_seconds) * COOLDOWN_MAX_PENALTY / COOLDOWN_SECONDS
    
    def get_both_cooldown_penalty(rank: InternalRank) -> float:
        penalty = get_single_cooldown_penalty(rank)
        if rank.counter_rank is not None:
            return penalty
        counter_penalty = get_single_cooldown_penalty(rank.counter_rank)
        return max(penalty, counter_penalty)

    def get_effective_value(rank: InternalRank) -> float:
        last_use = rank.last_use_datetime
        if last_use is None:
            return datetime_to_timestamp(now_dt)
        epoch_seconds = datetime_to_timestamp(last_use)
        return epoch_seconds - get_both_cooldown_penalty(rank)

    def get_cached_value(rank: InternalRank):
        cached = value_cache.get(rank.rankId)
        if cached is not None:
            return cached
        value = get_effective_value(rank)
        value_cache[rank.rankId] = value
        return value

    def compare(r1: InternalRank, r2: InternalRank) -> float:
        v1 = get_cached_value(r1)
        v2 = get_cached_value(r2)
        return v2 - v1

    return compare
