from constants import *
from cluster_creator import ClusterCreator
from path_solver import PathSolver
from visualizer import Visualizer

class TargetBankManager:
    def __init__(self):
        self.cluster_creator = ClusterCreator(x_start=0, z_start=0,
                                              width=REF, height=REF,
                                              window_width=RS_WIDTH, window_height=RS_HEIGHT,
                                              shift_size=SHIFT_SIZE)
        self.path_solver = PathSolver()
        self.visualizer = Visualizer()
        self.clusters = []

    def update_targets(self, targets):
        self.cluster_creator.fill_optional_clusters(targets)
        self.clusters = self.cluster_creator.select_clusters()
        self.path_solver.update_clusters(self.clusters)

    def visualize(self):
        i = 0
        for cluster in self.clusters:
            targets = cluster.get_target_list()
            self.visualizer.import_spheres_from_array(targets, self.visualizer.colors[i])
            i += 1
        # path
        order = self.path_solver.nearest_neighbor()
        self.visualizer.import_path_from_array(order)
        self.visualizer.finished_updating()


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance

@singleton
class getTargetBankManager(TargetBankManager):
    pass