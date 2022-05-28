class Post:
    def __init__(self, _id, _post_type_id, _creation_date, _score, _view_count, _body, _owner_user_id,
                 _last_activity_date, _title, _tags, _answer_count, _comment_count, _favorite_count, _content_license):
        self.id = int(_id)
        self.postTypeId = int(_post_type_id)
        self.creationDate = _creation_date
        self.score = int(_score)
        self.viewCount = int(_view_count) if _view_count is not None else None
        self.body = _body
        self.ownerUserId = int(_owner_user_id) if _owner_user_id is not None else None
        self.lastActivityData = _last_activity_date
        self.title = _title
        self.tags = _tags
        self.answerCount = int(_answer_count) if _answer_count is not None else None
        self.commentCount = int(_comment_count)
        self.favoriteCount = int(_favorite_count) if _favorite_count is not None else None
        self.contentLicense = _content_license

    @staticmethod
    def create(node):
        return Post(
            node.get("Id"),
            node.get("PostTypeId"),
            node.get("CreationDate"),
            node.get("Score"),
            node.get("ViewCount"),
            node.get("Body"),
            node.get("OwnerUserId"),
            node.get("LastActivityDate"),
            node.get("Title"),
            node.get("Tags"),
            node.get("AnswerCount"),
            node.get("CommentCount"),
            node.get("FavoriteCount"),
            node.get("ContentLicense")
        )
