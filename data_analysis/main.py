from dbo.data_repository import DataRepository
from showcase.rocket_showcase import rocket_showcase
from utils.utils import Mailbox


if __name__ == "__main__":
    Mailbox.debugLevel = 1

    # .meta files are shorter - exchange later for normal size archives
    data_sources = [
        {"dirname": "3dprinting", "url": "https://archive.org/download/stackexchange/3dprinting.meta.stackexchange.com.7z"},
        {"dirname": "android", "url": "https://archive.org/download/stackexchange/android.meta.stackexchange.com.7z"}
    ]

    data_repository = DataRepository(_data_sources=data_sources, _data_directory="../../data", _caching=True)
    data_repository.load_data_sets()

    rocket_showcase(data_repository)
