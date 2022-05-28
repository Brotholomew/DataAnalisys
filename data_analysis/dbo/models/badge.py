class Badge:
    def __init__(self, _id, _user_id, _name, _date, _class, _tag_based):
        self.id = int(_id)
        self.userId = int(_user_id)
        self.name = _name
        self.cls = _class  # class variable is forbidden
        self.tagBased = _tag_based

    @staticmethod
    def create(node):
        return Badge(
            node.get("Id"),
            node.get("UserId"),
            node.get("Name"),
            node.get("Date"),
            node.get("Class"),
            node.get("TagBased")
        )
