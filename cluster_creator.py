import math


class Cluster:
    def __init__(self, z_start, x_start, width, height):
        self.x_start = x_start
        self.z_start = z_start
        self.width = width
        self.height = height
        self.targets = []

    def add_target(self, target):
        self.targets.append(target)

    def get_target_list(self):
        return self.targets

    def get_position(self):
        z = self.z_start + (self.height / 2)
        x = self.x_start + (self.width / 2)
        t = self.get_min_t
        return (z, x, t)

    def get_min_t(self):
        min_t = self.targets[0][2]
        for target in self.targets:
            min_t = min(min_t, target[2])
        return min_t

    def get_max_t(self):
        max_t = self.targets[0][2]
        for target in self.targets:
            max_t = max(max_t, target[2])
        return max_t

    def get_x_start(self):
        return self.x_start

    def get_z_start(self):
        return self.z_start

    def is_target_in_range(self, target_z, target_x):
        if target_z < self.z_start or target_z > self.z_start + self.height:
            return False
        if target_x < self.x_start or target_x > self.x_start + self.width:
            return False
        return True


class ClusterCreator:
    def __init__(self, window_width, window_height, shift_size):
        self.window_width = window_width
        self.window_height = window_height
        self.shift_size = shift_size

    def set_motor_range(self, z_start, x_start, width, height):
        self.z_start = z_start
        self.x_start = x_start
        self.width = width
        self.height = height
        self.optional_clusters = []
        self.create_optional_clusters()

    def create_optional_clusters(self):
        num_of_windows_horizontal = self.width / self.shift_size
        num_of_windows_vertical = self.height / self.shift_size
        current_z = self.z_start
        for i in range (math.ceil(num_of_windows_vertical)):
            current_x = self.x_start
            for i in range (math.ceil(num_of_windows_horizontal)):
                if current_x + self.window_width > self.width or current_z + self.window_height > self.height:
                    continue
                current_width = min(self.window_width, self.width - current_x)
                current_height = min(self.window_height, self.height - current_z)
                window = Cluster(current_z, current_x, current_width, current_height)
                self.optional_clusters.append(window)
                current_x += self.shift_size
            current_z += self.shift_size

    def set_targets(self, targets):
        self.reset()
        for cluster in self.optional_clusters:
            for target in targets:
                if cluster.is_target_in_range(target[0], target[1]):
                    cluster.add_target(target)

    def get_cluster_by_target_list(self, target_list):
        splitted_items = []
        for item in target_list:
            item = item.split(" ")
            splitted_items.append([float(item[0]), float(item[1]), float(item[2])])
        for cluster in self.optional_clusters:
            current_target_list = cluster.get_target_list()
            if splitted_items == current_target_list:
                return cluster
        return None

    def get_subsets(self):
        return self.optional_clusters

    def get_universe(self):
        universe = []
        for cluster in self.optional_clusters:
            universe.extend(cluster.get_target_list())
        universe_as_str = []
        for item in universe:
            universe_as_str.append(f"{item[0]} {item[1]} {item[2]}")
        universe_as_str = list(dict.fromkeys(universe_as_str))
        return universe_as_str

    def set_cover(self, universe, subsets):
        elements = set(e for s in subsets for e in s)
        if elements != set(universe):
            return None
        covered = set()
        cover = []
        while covered != elements:
            subset = max(subsets, key=lambda s: len(set(s) - covered))
            cover.append(subset)
            covered |= set(subset)
        return cover

    # select the clusters using the set cover greedy approximation algorithm.
    def select_clusters(self):
        universe = self.get_universe()
        subsets = []
        for cluster in self.optional_clusters:
            target_list = cluster.get_target_list()
            new_list = []
            for item in target_list:
                new_list.append(f"{item[0]} {item[1]} {item[2]}")
            subsets.append(new_list)
        cover = self.set_cover(universe, subsets)
        clusters = []
        for target_list in cover:
            cluster = self.get_cluster_by_target_list(target_list)
            clusters.append(cluster)
        return clusters

    def reset(self):
        self.targets = []
        self.optional_clusters = []
        self.create_optional_clusters()