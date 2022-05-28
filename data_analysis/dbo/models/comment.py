class Comment:
    def __init__(self, _id, _post_id, _score, _text, _creation_date, _user_id, _content_license):
        self.id = int(_id)
        self.postId = int(_post_id)
        self.score = int(_score)
        self.text = _text
        self.creationDate = _creation_date
        self.userId = int(_user_id) if _user_id is not None else None
        self.contentLicense = _content_license

    @staticmethod
    def create(node):
        return Comment(
            node.get("Id"),
            node.get("PostId"),
            node.get("Score"),
            node.get("Text"),
            node.get("CreationDate"),
            node.get("UserId"),
            node.get("ContentLicense"),
        )
