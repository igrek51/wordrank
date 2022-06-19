from prometheus_client import Counter

metric_good_answers = Counter(
    'wordrank_good_answers',
    'total number of good answers',
)
metric_bad_answers = Counter(
    'wordrank_bad_answers',
    'total number of bad answers',
)
metric_all_answers = Counter(
    'wordrank_all_answers',
    'total number of all answers',
)
metric_word_added = Counter(
    'wordrank_word_added',
    'total number of added words',
)
