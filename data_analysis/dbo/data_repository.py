import os
import wget
import py7zr
import shutil

from data_analysis.dbo.data_set import DataSet
from ..utils.utils import Mailbox


class DataRepository:
    def __init__(self, _data_sources=None, _data_directory="../../data", _caching=False):
        self.data_sources = _data_sources
        self.data_sets = []

        self.data_directory = _data_directory
        self.caching = _caching

        # clean data_directory if caching disabled
        if not self.caching and os.path.exists(self.data_directory):
            shutil.rmtree(self.data_directory)
            Mailbox.debug("deleted data dir")

        try:
            os.mkdir(self.data_directory)
            Mailbox.debug("created data dir")
        except FileExistsError:
            pass

    def load_archive(self, url, dirname):
        download_path = f"{self.data_directory}/{dirname}"
        download_archive = f"{self.data_directory}/{dirname}/{dirname}.7z"

        # if the archive is downloaded and caching is enabled, skip downloading
        if self.caching and \
                os.path.exists(download_path) and \
                os.path.exists(os.path.join(download_path, "Comments.xml")) and \
                os.path.exists(os.path.join(download_path, "PostHistory.xml")) and \
                os.path.exists(os.path.join(download_path, "PostLinks.xml")) and \
                os.path.exists(os.path.join(download_path, "Tags.xml")) and \
                os.path.exists(os.path.join(download_path, "Votes.xml")) and \
                os.path.exists(os.path.join(download_path, "Badges.xml")) and \
                os.path.exists(os.path.join(download_path, "Users.xml")) and \
                os.path.exists(os.path.join(download_path, "Posts.xml")):
            Mailbox.debug(f"found cached data for set: {dirname}")
            return

        # remove potential old files
        if os.path.exists(download_path):
            shutil.rmtree(download_path)
            Mailbox.debug(f"removed dir {download_path}")

        try:
            os.mkdir(download_path)
            Mailbox.debug(f"created dir {download_path}")
        except FileExistsError:
            pass

        # download archive to data directory
        filename = wget.download(url=url, out=download_archive, bar=Mailbox.bar_progress)
        Mailbox.debug(f"downloaded archive {filename}")

        # extract archive
        archive = py7zr.SevenZipFile(filename, mode='r')
        archive.extractall(path=download_path)
        archive.close()
        Mailbox.debug(f"unpacked archive {filename}")

        # delete archive
        if not self.caching:
            os.remove(filename)
            Mailbox.debug(f"remove archive {filename}")

    def load_data(self, url, dirname):
        self.load_archive(url, dirname)

        data_set = DataSet(_data_directory=f"{self.data_directory}/{dirname}", _caching=self.caching)
        Mailbox.debug(f"created data set for {dirname}")
        return data_set

    def load_data_sets(self):
        for t in self.data_sources:
            data_set = self.load_data(t.get("url", None), t.get("dirname", None))
            self.data_sets.append(data_set)
