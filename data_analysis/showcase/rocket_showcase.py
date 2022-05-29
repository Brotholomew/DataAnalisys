import numpy as np

from clusters.cluster_collection import ClusterCollection
from clusters.clustrify_data import clustrify_data
from sklearn.linear_model import RidgeClassifierCV
from sklearn.metrics import accuracy_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sktime.transformations.panel.rocket import Rocket
from sklearn.ensemble import RandomForestClassifier
# from sktime.sktime.transformations.panel.rocket import Rocket
import pandas as pd


def padding(vector, reference_length):
    assert(len(vector) <= reference_length)

    if len(vector) == reference_length:
        return vector

    missing = reference_length - len(vector)
    complement = np.repeat(0, missing)
    return np.concatenate((vector, complement), axis=None)


def prepare_rocket_data(data_set, data_table, center_selector, num_of_clusters, property_selector):
    cluster_objects = clustrify_data(data_set, data_table, center_selector)
    cluster_collection = ClusterCollection(cluster_objects, num_of_clusters)

    classes = [cluster.center for cluster in cluster_collection.clusters]
    lengths = [len(cluster.objects) for cluster in cluster_collection.clusters]

    reference_length = max(lengths)

    data = []
    for cluster in cluster_collection.clusters:
        d = [property_selector(data_set, obj) for obj in cluster.objects]
        v = np.sort(padding(d, reference_length))
        data.append(pd.Series(v))

    #data = pd.DataFrame(data)
    data = pd.DataFrame({"dim0": data})
    #
    # x = np.shape(data)[0]
    # z = np.shape(data)[1]
    #
    # data = np.reshape(data, (x, 1, z))

    return data, classes


def unpack_data(data):
    temp = []
    for d in data["dim0"]:
        temp.append(d)

    return np.array(temp)


def data_extra_padding_internal(data, reference_length):
    if np.shape(data)[1] == reference_length:
        return data

    temp = []
    for d in data:
        temp.append(np.sort(padding(d, reference_length)))

    return np.array(temp)


def data_extra_padding(data1, data2):
    reference_length = max(np.shape(data1)[1], np.shape(data2)[1])
    return data_extra_padding_internal(data1, reference_length), data_extra_padding_internal(data2, reference_length)


def ridge_regression_fit_score_post_length(data_repository):
    num_of_clusters = 20
    num_of_classes = 10

    train_post_data, train_post_classes = prepare_rocket_data(
        data_repository.data_sets[0],
        data_repository.data_sets[0].posts,
        lambda data_set, data: data.score,
        num_of_clusters,
        lambda data_set, obj: len(obj.object.body)
    )
    train_post_data = unpack_data(train_post_data)

    test_post_data, test_post_classes = prepare_rocket_data(
        data_repository.data_sets[1],
        data_repository.data_sets[1].posts,
        lambda data_set, data: data.score,
        num_of_clusters,
        lambda data_set, obj: len(obj.object.body)
    )
    test_post_data = unpack_data(test_post_data)

    ck = num_of_clusters / num_of_classes
    classes = np.array([])
    for c in np.arange(1, num_of_classes + 1):
        classes = np.concatenate((classes, np.repeat(c, ck)), axis=None)

    train_post_data, test_post_data = data_extra_padding(train_post_data, test_post_data)

    classifier = make_pipeline(
        StandardScaler(with_mean=False),
        RidgeClassifierCV(alphas=np.logspace(-3, 3, 10)),
    )
    classifier.fit(train_post_data, classes)

    predictions = classifier.predict(test_post_data)
    accuracy = accuracy_score(predictions, classes)

    print(accuracy)


def rocket_score_post_length(data_repository):
    num_of_clusters = 40
    num_of_classes = 10

    train_post_data, train_post_classes = prepare_rocket_data(
        data_repository.data_sets[0],
        data_repository.data_sets[0].posts,
        lambda data_set, data: data.score,
        num_of_clusters,
        lambda data_set, obj: len(obj.object.body)
    )

    test_post_data, test_post_classes = prepare_rocket_data(
        data_repository.data_sets[1],
        data_repository.data_sets[1].posts,
        lambda data_set, data: data.score,
        num_of_clusters,
        lambda data_set, obj: len(obj.object.body)
    )

    ck = num_of_clusters / num_of_classes
    classes = np.array([])
    for c in np.arange(1, num_of_classes + 1):
        classes = np.concatenate((classes, np.repeat(c, ck)), axis=None)

    r = Rocket(500)
    r.fit(train_post_data)
    train_data_transformed = r.transform(train_post_data)
    test_data_transformed = r.transform(test_post_data)

    classifier = make_pipeline(
        StandardScaler(with_mean=False),
        RidgeClassifierCV(alphas=np.logspace(-3, 3, 10)),
    )
    classifier.fit(train_data_transformed, classes)

    predictions = classifier.predict(test_data_transformed)
    accuracy = accuracy_score(predictions, classes)

    print(accuracy)


def rocket_score_viewcount(data_repository):
    num_of_clusters = 20
    num_of_classes = 10

    train_post_data, train_post_classes = prepare_rocket_data(
        data_repository.data_sets[0],
        data_repository.data_sets[0].posts,
        lambda data_set, data: data.score,
        num_of_clusters,
        lambda data_set, obj: obj.object.viewCount
    )

    test_post_data, test_post_classes = prepare_rocket_data(
        data_repository.data_sets[1],
        data_repository.data_sets[1].posts,
        lambda data_set, data: data.score,
        num_of_clusters,
        lambda data_set, obj: obj.object.viewCount
    )

    ck = num_of_clusters / num_of_classes
    classes = np.array([])
    for c in np.arange(1, num_of_classes + 1):
        classes = np.concatenate((classes, np.repeat(c, ck)), axis=None)

    r = Rocket(500)
    r.fit(train_post_data)
    train_data_transformed = r.transform(train_post_data)
    test_data_transformed = r.transform(test_post_data)

    classifier = make_pipeline(
        StandardScaler(with_mean=False),
        RidgeClassifierCV(alphas=np.logspace(-3, 3, 10)),
    )
    classifier.fit(train_data_transformed, classes)

    predictions = classifier.predict(test_data_transformed)
    accuracy = accuracy_score(predictions, classes)

    print(accuracy)


def ridge_regression_fit_score_viewcount(data_repository):
    num_of_clusters = 20
    num_of_classes = 10

    train_post_data, train_post_classes = prepare_rocket_data(
        data_repository.data_sets[0],
        data_repository.data_sets[0].posts,
        lambda data_set, data: data.score,
        num_of_clusters,
        lambda data_set, obj: obj.object.viewCount
    )
    train_post_data = unpack_data(train_post_data)

    test_post_data, test_post_classes = prepare_rocket_data(
        data_repository.data_sets[1],
        data_repository.data_sets[1].posts,
        lambda data_set, data: data.score,
        num_of_clusters,
        lambda data_set, obj: obj.object.viewCount
    )
    test_post_data = unpack_data(test_post_data)

    ck = num_of_clusters / num_of_classes
    classes = np.array([])
    for c in np.arange(1, num_of_classes + 1):
        classes = np.concatenate((classes, np.repeat(c, ck)), axis=None)

    train_post_data, test_post_data = data_extra_padding(train_post_data, test_post_data)

    classifier = make_pipeline(
        StandardScaler(with_mean=False),
        RidgeClassifierCV(alphas=np.logspace(-3, 3, 10)),
    )
    classifier.fit(train_post_data, classes)

    predictions = classifier.predict(test_post_data)
    accuracy = accuracy_score(predictions, classes)

    print(accuracy)