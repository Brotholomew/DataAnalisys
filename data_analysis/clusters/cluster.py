from functools import reduce


class Cluster:
    def __init__(self, _center):
        self.center = _center
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, _obj):
        self.objects.remove(_obj)

    def update(self):
        if len(self.objects) == 0:
            self.center = 0
            return

        s = 0
        for obj in self.objects:
            s += obj.center

        self.center = s / len(self.objects)
