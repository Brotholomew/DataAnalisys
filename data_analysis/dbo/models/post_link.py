class PostLink:
    def __init__(self, _id, _creation_date, _post_id, _related_post_id, _link_type_id):
        self.id = int(_id)
        self.creationDate = _creation_date
        self.postId = int(_post_id)
        self.relatedPostId = int(_related_post_id)
        self.linkTypeId = int(_link_type_id)

    @staticmethod
    def create(node):
        return PostLink(
            node.get("Id"),
            node.get("CreationDate"),
            node.get("PostId"),
            node.get("RelatedPostId"),
            node.get("LinkTypeId")
        )
