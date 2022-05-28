class Vote:
    def __init__(self, _id, _post_id, _vote_type_id, _creation_date):
        self.id = int(_id)
        self.postId = int(_post_id)
        self.voteTypeId = int(_vote_type_id)
        self.creationDate = _creation_date

    @staticmethod
    def create(node):
        return Vote(
            node.get("Id"),
            node.get("PostId"),
            node.get("VoteTypeId"),
            node.get("CreationDate")
        )
