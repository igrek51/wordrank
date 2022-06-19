from prometheus_client import Counter

metric_good_answers = Counter(
    'webdict_good_answers',
    'total number of good answers',
)
metric_bad_answers = Counter(
    'webdict_bad_answers',
    'total number of bad answers',
)
metric_all_answers = Counter(
    'webdict_all_answers',
    'total number of all answers',
)
metric_word_added = Counter(
    'webdict_word_added',
    'total number of added words',
)
