from data_analysis.clusters.cluster_collection import ClusterCollection
from data_analysis.dbo.data_repository import DataRepository
from utils.utils import Mailbox
from clusters.clustrify_data import clustrify_data

if __name__ == "__main__":
    Mailbox.debugLevel = 1

    # .meta files are shorter - exchange later for normal size archives
    data_sources = [
        {"dirname": "3dprinting", "url": "https://archive.org/download/stackexchange/3dprinting.meta.stackexchange.com.7z"},
        {"dirname": "android", "url": "https://archive.org/download/stackexchange/android.meta.stackexchange.com.7z"}
    ]

    data_repository = DataRepository(_data_sources=data_sources, _data_directory="../../data", _caching=True)
    data_repository.load_data_sets()

    cluster_objects = clustrify_data(
        data_repository.data_sets[0],
        data_repository.data_sets[0].posts,
        lambda data_set, data: data.score
    )
    post_score_clusters = ClusterCollection(cluster_objects, 20)

    print(data_repository.data_sets)
