class User:
    def __init__(self, _id, _reputation, _creation_date, _display_name, _last_access_date, _location, _about_me, _views,
                 _up_votes, _down_votes, _account_id):
        self.id = int(_id)
        self.reputation = _reputation
        self.creationDate = _creation_date
        self.displayName = _display_name
        self.lastAccessDate = _last_access_date
        self.location = _location
        self.aboutMe = _about_me
        self.views = int(_views)
        self.upVotes = int(_up_votes)
        self.downVotes = int(_down_votes)
        self.accountId = int(_account_id)

    @staticmethod
    def create(node):
        return User(
            node.get("Id"),
            node.get("Reputation"),
            node.get("CreationDate"),
            node.get("DisplayName"),
            node.get("LastAccessDate"),
            node.get("Location"),
            node.get("AboutMe"),
            node.get("Views"),
            node.get("UpVotes"),
            node.get("DownVotes"),
            node.get("AccountId")
        )
