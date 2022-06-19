from wordrank.api.dto.rank import InternalRank
from wordrank.djangoapp.words.time import seconds_ago


COOLDOWN_SECONDS = 30 * 60
COOLDOWN_MAX_PENALTY = 1000


def make_hardest_word_comparator():
    value_cache = {}

    def get_single_cooldown_penalty(rank: InternalRank) -> float:
        if rank.last_use_datetime is None:
            return 0

        elapsed_seconds = seconds_ago(rank.last_use_datetime)
        
        if elapsed_seconds >= COOLDOWN_SECONDS:
            return 0
        
        return (COOLDOWN_SECONDS - elapsed_seconds) * COOLDOWN_MAX_PENALTY / COOLDOWN_SECONDS
    
    def get_effective_value(rank: InternalRank) -> float:
        return float(rank.triesCount) - get_single_cooldown_penalty(rank)

    def get_cached_value(rank: InternalRank):
        cached = value_cache.get(rank.rankId)
        if cached is not None:
            return cached
        value = get_effective_value(rank)
        value_cache[rank.rankId] = value
        return value

    def compare(r1: InternalRank, r2: InternalRank) -> float:
        f1 = get_cached_value(r1)
        f2 = get_cached_value(r2)
        if f1 != f2:
            return (f2 - f1) * 20

        # higher rank
        if r1.rankValue != r2.rankValue:
            return r2.rankValue - r1.rankValue
        
        # prior - words which were never used (no last use)
        if r1.last_use_datetime is None and r2.last_use_datetime is None:
            return 0
        if r1.last_use_datetime is None:
            return -10
        if r2.last_use_datetime is None:
            return 10
        
        return 0

    return compare
