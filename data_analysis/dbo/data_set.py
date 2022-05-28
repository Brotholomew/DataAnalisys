import os

from xml.etree import ElementTree as et

from .models.comment import Comment
from .models.badge import Badge
from .models.post import Post
from .models.post_history import PostHistory
from .models.post_link import PostLink
from .models.tag import Tag
from .models.user import User
from .models.vote import Vote


class DataSet:
    def __init__(self, _data_directory="../../data", _caching=False):
        self.caching = _caching

        self.comments = None
        self.postHistory = None
        self.postLinks = None
        self.tags = None
        self.users = None
        self.votes = None
        self.badges = None
        self.posts = None

        self.files = {
            "comments":     {"file": f"./{_data_directory}/Comments.xml",      "constructor": lambda node: Comment.create(node)},
            "postHistory":  {"file": f"./{_data_directory}/PostHistory.xml",   "constructor": lambda node: PostHistory.create(node)},
            "postLinks":    {"file": f"./{_data_directory}/PostLinks.xml",     "constructor": lambda node: PostLink.create(node)},
            "tags":         {"file": f"./{_data_directory}/Tags.xml",          "constructor": lambda node: Tag.create(node)},
            "votes":        {"file": f"./{_data_directory}/Votes.xml",         "constructor": lambda node: Vote.create(node)},
            "badges":       {"file": f"./{_data_directory}/Badges.xml",        "constructor": lambda node: Badge.create(node)},
            "users":        {"file": f"./{_data_directory}/Users.xml",         "constructor": lambda node: User.create(node)},
            "posts":        {"file": f"./{_data_directory}/Posts.xml",         "constructor": lambda node: Post.create(node)},
        }

        self.load_sets()
        self.init_cleanup()

    def set_set(self, name, value):
        if   name == "comments":
            self.comments = value
        elif name == "postHistory":
            self.postHistory = value
        elif name == "postLinks":
            self.postLinks = value
        elif name == "tags":
            self.tags = value
        elif name == "votes":
            self.votes = value
        elif name == "badges":
            self.badges = value
        elif name == "users":
            self.users = value
        elif name == "posts":
            self.posts = value

    @staticmethod
    def load_data(file, constructor):
        res = []

        tree = et.parse(file)
        root = tree.getroot()

        for node in root:
            res.append(constructor(node))

        return res

    def init_cleanup(self):
        if self.caching:
            return

        for file in self.files.values():
            os.remove(file.get("file", ""))

    def load_sets(self):
        for k, v in self.files.items():
            self.set_set(k, DataSet.load_data(v["file"], v["constructor"]))
