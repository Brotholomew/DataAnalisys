import math
import pickle

from clusters.cluster_collection import ClusterCollection
from clusters.clustrify_data import clustrify_data
from dbo.data_repository import DataRepository

import matplotlib.pyplot as plt
import numpy as np
import os


def most_frequent(lst):
    return max(set(lst), key=lst.count)


def prepare_cluster_data(data_set, data_table, center_selector, num_of_clusters):
    cluster_objects = clustrify_data(data_set, data_table, center_selector)
    cluster_collection = ClusterCollection(cluster_objects, num_of_clusters)
    classes = [cluster.center for cluster in cluster_collection.clusters]

    return cluster_collection, classes


def cluster2_internal(data_repository, idx, data_set_selector, object_selector0, object_selector1, num_of_clusters=20,
                      num_of_classes=10, title1="", title2="", title3="", y1="", y2="", y3="", filename=""):
    ck = num_of_clusters / num_of_classes
    classes = np.array([])
    for c in np.arange(1, num_of_classes + 1):
        classes = np.concatenate((classes, np.repeat(c, ck)), axis=None)

    cluster_collection_score, cluster_classes_score = prepare_cluster_data(
        data_repository.data_sets[idx],
        data_set_selector(data_repository.data_sets[idx]),
        object_selector0,
        num_of_clusters
    )

    cluster_collection_length, cluster_classes_length = prepare_cluster_data(
        data_repository.data_sets[idx],
        data_set_selector(data_repository.data_sets[idx]),
        object_selector1,
        num_of_clusters
    )

    cluster2_data0 = []
    for cluster in cluster_collection_score.clusters:
        t = [object_selector0(data_repository.data_sets[idx], obj.object) for obj in cluster.objects]
        cluster2_data0.append(t)

    cluster2_data1 = []
    for cluster in cluster_collection_length.clusters:
        t = [object_selector1(data_repository.data_sets[idx], obj.object) for obj in cluster.objects]
        cluster2_data1.append(t)

    cluster2 = []
    for cluster in cluster_collection_score.clusters:
        temp = []
        for obj in cluster.objects:
            tt = None
            for idx, cc in enumerate(cluster_collection_length.clusters):
                for oo in cc.objects:
                    if obj.object == oo.object:
                        tt = classes[idx]
                        break

                if tt is not None:
                    break

            temp.append(tt)

        cluster2.append(temp)

    temp = []
    temp2 = []
    temp3 = []
    for idx, c in enumerate(np.arange(0, num_of_classes)):
        t = []
        t2 = []
        t3 = []
        for i in np.arange(0, ck):
            t.append(cluster2[int(idx * ck + i)])
            t2.append(cluster2_data0[int(idx * ck + i)])
            t3.append(cluster2_data1[int(idx * ck + i)])
        t = [item for sublist in t for item in sublist]
        t2 = [item for sublist in t2 for item in sublist]
        t3 = [item for sublist in t3 for item in sublist]
        temp.append(t)
        temp2.append(t2)
        temp3.append(t3)

    cluster2 = np.array(temp)
    cluster2_data0 = np.array(temp2)
    cluster2_data1 = np.array(temp3)
    cls = np.arange(1, num_of_classes + 1)

    save_boxplot(title1, y1, cluster2_data0, cls, filename)
    save_boxplot(title2, y2, cluster2_data1, cls, filename)
    save_barplot(title3, y3, cluster2, cls, filename)

    return cluster2


def save_boxplot(title, y, data, xlabels, filename):
    fig1, ax1 = plt.subplots()

    ax1.boxplot(
        x=data,
        labels=xlabels
    )
    ax1.set_ylabel(y)
    ax1.set_title(title)

    try:
        os.mkdir("../plots")
    except FileExistsError:
        pass

    plt.savefig(f"../plots/{filename}_{title}.png")


def save_barplot(title, y, data, xlabels, filename):
    fig1, ax1 = plt.subplots()

    temp = []
    temp2 = []
    for x in xlabels:
        t = []
        t2 = []
        for row in data:
            unique, counts = np.unique(row, return_counts=True)
            tt = dict(zip(unique, counts))
            t.append(tt.get(x, 0))
            s = sum(counts)
            t2.append(math.trunc((tt.get(x, 0) / s) * 100))

        temp.append(t)
        temp2.append(t2)

    sums = None
    sums2 = None
    for idx, row in enumerate(temp):
        if sums is None:
            sums = [row]
        else:
            prev = sums[-1]
            r = [d + prev[i] for i, d in enumerate(row)]
            sums.append(r)

        if sums2 is None:
            sums2 = [temp2[idx]]
        else:
            prev = sums2[-1]
            r = [d + prev[i] for i, d in enumerate(temp2[idx])]
            sums2.append(r)

    for idx, r in enumerate(sums2[-1]):
        if r != 100:
            i = -1
            while temp2[i] == 0:
                i -= 1

            temp2[i][idx] += 100 - r

    for idx, row in enumerate(temp):
        bottom = None
        if idx > 0:
            bottom = sums[idx - 1]
        ax1.bar(x=xlabels, height=row, label=f"{xlabels[idx]}", bottom=bottom)

    ax1.set_ylabel("number of observations from clusters")
    ax1.set_title(title)
    ax1.legend()

    try:
        os.mkdir("../plots")
    except FileExistsError:
        pass

    plt.savefig(f"../plots/{filename}_{title}.png")

    fig1, ax1 = plt.subplots()
    for idx, row in enumerate(temp2):
        bottom = None
        if idx > 0:
            bottom = sums2[idx - 1]
        ax1.bar(x=xlabels, height=row, label=f"{xlabels[idx]}", bottom=bottom)

    ax1.set_ylabel("% of observations from clusters")
    ax1.legend(loc='center left', bbox_to_anchor=(0.96, 0.5))
    ax1.set_title(f"{title} (%)")

    plt.savefig(f"../plots/{filename}_{title}_percentage.png")


def cluster2_score_length(data_repository, index, num_of_clusters=20, num_of_classes=10, filename=""):
    return cluster2_internal(
        data_repository,
        index,
        lambda data_set: data_set.posts,
        lambda data_set, data: data.score,
        lambda data_set, data: len(data.body),
        num_of_clusters,
        num_of_classes,
        "K-means Clusters by post's score",
        "K-means Clusters by post's length",
        "Cluster2 algorithm results by post's score x length",
        "post's score",
        "post's length",
        "length cluster number",
        f"{filename}_score_length"
    )


def cluster2_score_hour(data_repository, index, num_of_clusters=20, num_of_classes=10, filename=""):
    return cluster2_internal(
        data_repository,
        index,
        lambda data_set: data_set.posts,
        lambda data_set, data: data.score,
        lambda data_set, data: data.creationDate.hour,
        num_of_clusters,
        num_of_classes,
        "K-means Clusters by post's score",
        "K-means Clusters by post's hour of creation",
        "Cluster2 algorithm results by post's score x hour of creation",
        "post's score",
        "post's hour of creation",
        "creation hour cluster number",
        f"{filename}_score_hour"
    )


def cluster2_vc_length(data_repository, index, num_of_clusters=20, num_of_classes=10, filename=""):
    return cluster2_internal(
        data_repository,
        index,
        lambda data_set: data_set.posts,
        lambda data_set, data: data.viewCount,
        lambda data_set, data: len(data.body),
        num_of_clusters,
        num_of_classes,
        "K-means Clusters by post's view count",
        "K-means Clusters by post's length",
        "Cluster2 algorithm results by post's view count x length",
        "post's view count",
        "post's length",
        "length cluster number",
        f"{filename}_vc_length"
    )


def cluster2_vc_hour(data_repository, index, num_of_clusters=20, num_of_classes=10, filename=""):
    return cluster2_internal(
        data_repository,
        index,
        lambda data_set: data_set.posts,
        lambda data_set, data: data.viewCount,
        lambda data_set, data: data.creationDate.hour,
        num_of_clusters,
        num_of_classes,
        "K-means Clusters by post's view count",
        "K-means Clusters by post's hour of creation",
        "Cluster2 algorithm results by post's view count x hour of creation",
        "post's view count",
        "post's creation hour",
        "creation hour cluster number",
        f"{filename}_vc_hour"
    )


def cluster2_test(data_repository, number_of_clusters, number_of_classes, fun, filenames, fun_name, y):
    cluster_results = []
    for i in np.arange(0, 6):
        cluster_results.append(fun(data_repository, 0, number_of_clusters, number_of_classes, filenames[i])),

    temp = []
    temp2 = []
    for idx in np.arange(0, number_of_classes):
        t = []

        for c in cluster_results:
            t.append(c[idx])

        t = [item for sublist in t for item in sublist]
        temp.append(t)

        unique, counts = np.unique(t, return_counts=True)
        tt = dict(zip(unique, counts))
        s = sum(tt.values())
        temp2.append(dict((k, v / s) for k, v in tt.items()))

    save_barplot(f"Cluster2 summary graph for {fun_name}", y, temp, np.arange(1, number_of_classes + 1), f"summary_graph_{fun_name}")
    pickle.dump(temp2, open(f"../plots/summary_{fun_name}.p", "wb"))


def cluster2_showcase():
    data_sources = [
        {"dirname": "3dprinting",
         "url": "https://archive.org/download/stackexchange/3dprinting.stackexchange.com.7z"},
        {"dirname": "android", "url": "https://archive.org/download/stackexchange/android.stackexchange.com.7z"},
        {"dirname": "apple", "url": "https://archive.org/download/stackexchange/apple.stackexchange.com.7z"},
        {"dirname": "winphone",
         "url": "https://archive.org/download/stackexchange/windowsphone.stackexchange.com.7z"},
        {"dirname": "bitcoin", "url": "https://archive.org/download/stackexchange/bitcoin.stackexchange.com.7z"},
        {"dirname": "ethereum", "url": "https://archive.org/download/stackexchange/ethereum.stackexchange.com.7z"}
        # {"dirname": "3dprinting",
        #  "url": "https://archive.org/download/stackexchange/3dprinting.meta.stackexchange.com.7z"},
        # {"dirname": "android", "url": "https://archive.org/download/stackexchange/android.meta.stackexchange.com.7z"},
        # {"dirname": "apple", "url": "https://archive.org/download/stackexchange/apple.meta.stackexchange.com.7z"},
        # {"dirname": "winphone",
        #  "url": "https://archive.org/download/stackexchange/windowsphone.meta.stackexchange.com.7z"},
        # {"dirname": "bitcoin", "url": "https://archive.org/download/stackexchange/bitcoin.meta.stackexchange.com.7z"},
        # {"dirname": "ethereum", "url": "https://archive.org/download/stackexchange/ethereum.meta.stackexchange.com.7z"}
    ]

    data_repository = DataRepository(_data_sources=data_sources, _data_directory="../../data", _caching=False)
    data_repository.load_data_sets()
    filenames = [src.get("dirname") for src in data_sources]
    functions = [cluster2_score_length, cluster2_score_hour, cluster2_vc_length, cluster2_vc_hour]
    fun_names = ["score_length", "score_hour", "vc_length", "vc_hour"]
    ys = ["length clusters", "hour clusters", "length clusters", "hour clusters"]

    for idx, fun in enumerate(functions):
        cluster2_test(data_repository, 20, 10, fun, filenames, fun_names[idx], ys[idx])
