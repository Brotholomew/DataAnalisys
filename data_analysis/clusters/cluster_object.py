class ClusterObject:
    def __init__(self, _center, _object):
        self.center = _center
        self.object = _object
        self.cluster = None

    def assign(self, cluster):
        if self.cluster is not None:
            if self.cluster == cluster:
                return False

            self.cluster.remove_object(self)

        self.cluster = cluster
        cluster.add_object(self)

        return True
