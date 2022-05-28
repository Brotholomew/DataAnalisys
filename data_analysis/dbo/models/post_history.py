class PostHistory:
    def __init__(self, _id, _post_history_type_id, _post_id, _revision_guid, _creation_date, _user_id, _text, _content_license):
        self.id = int(_id)
        self.postHistoryTypeId = int(_post_history_type_id)
        self.postId = int(_post_id)
        self.revisionGuid = _revision_guid
        self.creationDate = _creation_date
        self.userId = int(_user_id) if _user_id is not None else None
        self.text = _text
        self.contentLicense = _content_license

    @staticmethod
    def create(node):
        return PostHistory(
            node.get("Id"),
            node.get("PostHistoryTypeId"),
            node.get("PostId"),
            node.get("RevisionGuid"),
            node.get("CreationDate"),
            node.get("UserId"),
            node.get("Text"),
            node.get("ContentLicense")
        )
