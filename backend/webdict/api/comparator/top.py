from wordrank.api.dto.rank import InternalRank
from wordrank.djangoapp.words.time import seconds_ago


COOLDOWN_SECONDS = 10 * 60
COOLDOWN_MAX_PENALTY = 20


def make_top_word_comparator():
    rank_value_cache = {}

    def get_cached_rank_value(rank: InternalRank):
        cached = rank_value_cache.get(rank.rankId)
        if cached is not None:
            return cached
        value = get_effective_rank_value(rank)
        rank_value_cache[rank.rankId] = value
        return value

    def compare(r1: InternalRank, r2: InternalRank) -> float:
        f1 = get_cached_rank_value(r1)
        f2 = get_cached_rank_value(r2)
        if f1 != f2:
            return (f2 - f1) * 20
        
        # prior - words which were never used (no last use)
        if r1.last_use_datetime is None and r2.last_use_datetime is None:
            return 0
        if r1.last_use_datetime is None:
            return -10
        if r2.last_use_datetime is None:
            return 10
        
        # prior - words which were used more times (more difficult)
        if r1.triesCount != r2.triesCount:
            return r2.triesCount - r1.triesCount
        
        return 0

    return compare


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
    

def get_effective_rank_value(rank: InternalRank) -> float:
    return float(rank.rankValue) - get_both_cooldown_penalty(rank)
