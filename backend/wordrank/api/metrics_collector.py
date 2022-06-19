from prometheus_client.core import REGISTRY
from prometheus_client.metrics_core import GaugeMetricFamily

from wordrank.api.endpoint.stats import list_all_stats


def setup_metrics_collector():
    REGISTRY.register(MetricsCollector())


class MetricsCollector:

    def collect(self):

        all_stats = list_all_stats()
        for stat in all_stats:
            user_id = stat.user_id
            dict_code = stat.dict_code

            labels = {
                'user_id': user_id,
                'dict_code': dict_code,
            }

            labels['direction'] = 'straight'
            ranks = stat.straight_ranks
            yield _create_metric('wordrank_stats_all_count', ranks.allCount, labels)
            yield _create_metric('wordrank_stats_trained', ranks.trained.count, labels)
            yield _create_metric('wordrank_stats_training_in_progress', ranks.trainingInProgress.count, labels)
            yield _create_metric('wordrank_stats_touched', ranks.touched.count, labels)
            yield _create_metric('wordrank_stats_cooling_down', ranks.coolingDown.count, labels)
            yield _create_metric('wordrank_stats_rank_sum', ranks.rankSum, labels)

            labels['direction'] = 'reversed'
            ranks = stat.reversed_ranks
            yield _create_metric('wordrank_stats_all_count', ranks.allCount, labels)
            yield _create_metric('wordrank_stats_trained', ranks.trained.count, labels)
            yield _create_metric('wordrank_stats_training_in_progress', ranks.trainingInProgress.count, labels)
            yield _create_metric('wordrank_stats_touched', ranks.touched.count, labels)
            yield _create_metric('wordrank_stats_cooling_down', ranks.coolingDown.count, labels)
            yield _create_metric('wordrank_stats_rank_sum', ranks.rankSum, labels)

            labels['direction'] = 'both-way'
            ranks = stat.both_ranks
            yield _create_metric('wordrank_stats_all_count', ranks.allCount, labels)
            yield _create_metric('wordrank_stats_trained', ranks.trained.count, labels)
            yield _create_metric('wordrank_stats_training_in_progress', ranks.trainingInProgress.count, labels)
            yield _create_metric('wordrank_stats_touched', ranks.touched.count, labels)
            yield _create_metric('wordrank_stats_cooling_down', ranks.coolingDown.count, labels)
            yield _create_metric('wordrank_stats_rank_sum', ranks.rankSum, labels)


def _create_metric(name: str, value: float, labels) -> GaugeMetricFamily:
    metric = GaugeMetricFamily(name, name)
    metric.add_sample(name, labels, value)
    return metric
