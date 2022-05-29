import numpy as np

from .cluster import Cluster
from utils.utils import Mailbox


class ClusterCollection:
    def __init__(self, _objects, _num_of_clusters):
        if _num_of_clusters > len(_objects):
            Mailbox.debug(f"object list is shorted than the specified number of kernels! Trimming number of kernels to {len(_objects)}")

        self.objects = _objects
        self.num_of_clusters = min(len(_objects), _num_of_clusters)
        self.clusters = self.create_clusters()
        self.k_means()
        self.clusters.sort(key=lambda o: o.center)

    def create_clusters(self):
        values = set([obj.center for obj in self.objects])
        values = list(values)

        if len(values) < self.num_of_clusters:
            Mailbox.debug(f"There are not enough unique values in the object list! Cropping number of clusters to {self.num_of_clusters}")
            self.num_of_clusters = len(values)

        chosen = np.random.choice(values, size=self.num_of_clusters, replace=False)
        clusters = [Cluster(c) for c in chosen]

        return clusters

    def k_means(self):
        Mailbox.debug(f"began k-means algorithm for a set of {len(self.objects)} observations")
        changed = True
        while changed:
            changed = False

            # Assignment phase
            for obj in self.objects:
                distances = [{"distance": abs(obj.center - cluster.center), "cluster": cluster} for cluster in self.clusters]
                closest = min(distances, key=lambda t: t.get("distance", np.inf))
                changed = obj.assign(closest.get("cluster", None))

            # Update phase
            for cluster in self.clusters:
                cluster.update()

        Mailbox.debug(f"finished k-means algorithm for a set of {len(self.objects)} observations")
