from data_analysis.clusters.cluster_collection import ClusterCollection
from data_analysis.clusters.clustrify_data import clustrify_data


def prepare_rocket_data(data_set, data_table, center_selector, num_of_clusters, property_selector):
    cluster_objects = clustrify_data(data_set, data_table, center_selector)
    cluster_collection = ClusterCollection(cluster_objects, num_of_clusters)

    classes = [cluster.center for cluster in cluster_collection.clusters]
    lengths = [len(cluster.objects) for cluster in cluster_collection.clusters]

    reference_length = max(lengths)
