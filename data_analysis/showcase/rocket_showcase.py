import numpy as np

from clusters.cluster_collection import ClusterCollection
from clusters.clustrify_data import clustrify_data


def padding(vector, reference_length):
    assert(len(vector) <= reference_length)

    if len(vector) == reference_length:
        return vector

    missing = reference_length - len(vector)
    complement = np.repeat(-1, missing)
    return np.concatenate((vector, complement), axis=None)


def prepare_rocket_data(data_set, data_table, center_selector, num_of_clusters, property_selector):
    cluster_objects = clustrify_data(data_set, data_table, center_selector)
    cluster_collection = ClusterCollection(cluster_objects, num_of_clusters)

    classes = [cluster.center for cluster in cluster_collection.clusters]
    lengths = [len(cluster.objects) for cluster in cluster_collection.clusters]

    reference_length = max(lengths)

    data = np.array([])
    for cluster in cluster_collection.clusters:
        v = padding([property_selector(data_set, obj) for obj in cluster.objects], reference_length)
        np.concatenate((data, v), axis=0)

    x = np.shape(data)[0]
    z = np.shape(data)[2]

    data = np.reshape(data, (x, 1, z))

    return data, classes


def rocket_showcase(data_repository):
    post_data, post_classes = prepare_rocket_data(
        data_repository.data_sets[0],
        data_repository.data_sets[0].posts,
        lambda data_set, data: data.score,
        20,
        lambda data_set, obj: len(obj.object.body)
    )

    print(post_data)
