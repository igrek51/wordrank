from typing import Any, Callable, List, Optional

from webdict.djangoapp.words import models
from webdict.djangoapp.words.time import seconds_ago


COOLDOWN_SECONDS = 10 * 60
COOLDOWN_MAX_PENALTY = 20


def make_top_word_comparator():
    effective_rank_value_cache = {}

    def getCachedEffectiveRankValue(rank: models.Rank):
        rank_id = rank.id
        cached = effective_rank_value_cache.get(rank_id)
        if cached is not None:
            return cached

        value = getEffectiveRankValue(rank)
        effective_rank_value_cache[rank_id] = value
        return value
    
    def getSingleCooldownPenalty(rank: models.Rank) -> float:
        if rank.last_use is None:
            return 0

        elapsed_seconds = seconds_ago(rank.last_use)
        
        if elapsed_seconds >= COOLDOWN_SECONDS:
            return 0
        
        return (COOLDOWN_SECONDS - elapsed_seconds) * COOLDOWN_MAX_PENALTY / COOLDOWN_SECONDS
    
    def getBothCooldownPenalty(rank: models.Rank) -> float:
        # if !rank.getReversedRank().isPresent():
        # 	return getSingleCooldownPenalty(rank)
        # return Math.max(getSingleCooldownPenalty(rank), getSingleCooldownPenalty(rank.getReversedRank()
        # 		.get()))
        return getSingleCooldownPenalty(rank)
    
    def getEffectiveRankValue(rank: models.Rank) -> float:
        return rank.rank_value - getBothCooldownPenalty(rank)

    def compare(o1: models.Rank, o2: models.Rank) -> float:
        f1 = getCachedEffectiveRankValue(o1)
        f2 = getCachedEffectiveRankValue(o2)
        if f1 != f2:
            return (f2 - f1) * 20
        
        # prior - words which were never used (no last use)
        if o1.last_use is None and o2.last_use is None:
            return 0
        if o1.last_use is None:
            return -10
        if o2.last_use is None:
            return 10
        
        # prior - words which were used more times (more difficult)
        if o1.tries_count != o2.tries_count:
            return o2.tries_count - o1.tries_count
        
        return 0

    return compare
