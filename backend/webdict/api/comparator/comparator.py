from webdict.api.dto.rank import RankModel
from webdict.djangoapp.words.time import seconds_ago


COOLDOWN_SECONDS = 10 * 60
COOLDOWN_MAX_PENALTY = 20


def make_top_word_comparator():
    effective_rank_value_cache = {}

    def get_single_cooldown_penalty(rank: RankModel) -> float:
        if rank.last_use_datetime is None:
            return 0

        elapsed_seconds = seconds_ago(rank.last_use_datetime)
        
        if elapsed_seconds >= COOLDOWN_SECONDS:
            return 0
        
        return (COOLDOWN_SECONDS - elapsed_seconds) * COOLDOWN_MAX_PENALTY / COOLDOWN_SECONDS
    
    def get_both_cooldown_penalty(rank: RankModel) -> float:
        # if !rank.getReversedRank().isPresent():
        # 	return get_single_cooldown_penalty(rank)
        # return Math.max(get_single_cooldown_penalty(rank), get_single_cooldown_penalty(rank.getReversedRank()
        # 		.get()))
        return get_single_cooldown_penalty(rank)
    
    def get_effective_rank_value(rank: RankModel) -> float:
        return float(rank.rankValue) - get_both_cooldown_penalty(rank)

    def get_cached_effective_rank_value(rank: RankModel):
        cached = effective_rank_value_cache.get(rank.rankId)
        if cached is not None:
            return cached

        value = get_effective_rank_value(rank)
        effective_rank_value_cache[rank.rankId] = value
        return value

    def compare(r1: RankModel, r2: RankModel) -> float:
        f1 = get_cached_effective_rank_value(r1)
        f2 = get_cached_effective_rank_value(r2)
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
        if r1.tries_count != r2.tries_count:
            return r2.tries_count - r1.tries_count
        
        return 0

    return compare
