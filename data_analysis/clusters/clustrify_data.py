from .cluster_object import ClusterObject


def clustrify_data(data_set, data_table, selector):
    cluster_objects = []

    for data in data_table:
        cls = selector(data_set, data)
        cluster_object = ClusterObject(cls, data)

        cluster_objects.append(cluster_object)

    return cluster_objects
