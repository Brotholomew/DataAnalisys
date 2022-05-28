class Tag:
    def __init__(self, _id, _count, _is_required):
        self.id = int(_id)
        self.count = int(_count)
        self.isRequired = _is_required

    @staticmethod
    def create(node):
        return Tag(
            node.get("Id"),
            node.get("Count"),
            node.get("IsRequired")
        )
