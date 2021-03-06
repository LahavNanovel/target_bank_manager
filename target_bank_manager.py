from constants import *
from cluster_creator import ClusterCreator
from path_solver import PathSolver
from visualizer import Visualizer
# from cameras.camerasOffset.camerasOffset import getCamerasOffset, CamerasOffset


class TargetBankManager:
    def __init__(self):
        self.cluster_creator = ClusterCreator(window_width=RS_WIDTH,
                                              window_height=RS_HEIGHT,
                                              shift_size=SHIFT_SIZE)
        self.path_solver = PathSolver()
        self.visualizer = Visualizer()
        self.clusters = []

    def set_motor_range(self, range_dictionary: dict):
        self.z_start, self.z_end = range_dictionary["z_axis_range"]
        self.x_start, self.x_end = range_dictionary["x_axis_range"]
        self.t_start, self.t_end = range_dictionary["t_axis_range"]
        self.cluster_creator.set_motor_range(self.z_start,
                                             self.x_start,
                                             abs(self.x_start - self.x_end),
                                             abs(self.z_start - self.z_end))

    def is_point_in_range(self, point, z_offset, x_offset, t_offset):
        if (point[0] + z_offset) < self.z_start or (point[0] + z_offset) > self.z_end:
            return False
        if (point[1] + x_offset) < self.x_start or (point[1] + x_offset) > self.x_end:
            return False
        if (point[2] + t_offset) < self.t_start or (point[2] + t_offset) > self.t_end:
            return False
        return True

    def filter_out_of_range_points(self, points):
        # in_range = []
        # for point in points:
        #     getCamerasOffset().load_init_data()  # reload the data from the file
        #     z_offset = getCamerasOffset().get_offset(key_cam_offset=CamerasOffset.REMOTE_CAM_Z_OFFSET)
        #     x_offset = getCamerasOffset().get_offset(key_cam_offset=CamerasOffset.REMOTE_CAM_X_OFFSET)
        #     t_offset = getCamerasOffset().get_offset(key_cam_offset=CamerasOffset.REMOTE_CAM_T_OFFSET)
        #     if self.is_point_in_range(point, z_offset, x_offset, t_offset):
        #         in_range.append(point)
        # return in_range
        return points

    def sort_clusters_by_order(self, order):
        sorted_clusters = []
        for coordinate in order:
            for cluster in self.clusters:
                if cluster.get_position() == coordinate:
                    sorted_clusters.append(cluster)
        self.clusters = sorted_clusters

    def set_targets(self, targets):
        targets = self.filter_out_of_range_points(targets)
        self.cluster_creator.set_targets(targets)
        self.clusters = self.cluster_creator.select_clusters()
        order = self.path_solver.get_path(self.clusters, method="bottom_to_top")
        self.sort_clusters_by_order(order)
        for cluster in self.clusters:
            target_list = cluster.get_target_list()
            for target in target_list:
                self.visualizer.add_sphere(target)
            self.visualizer.add_bounding_box(cluster.get_x_start(),
                                             cluster.get_z_start(),
                                             cluster.get_min_t(),
                                             cluster.get_max_t())
        self.visualizer.add_path(order)

    def get_number_of_targets(self):
        # TODO: remove duplicates to return the correct number.
        targets = []
        for cluster in self.clusters:
            targets.extend(cluster.get_target_list())
        return len(targets)

    def get_next_cluster(self):
        self.active_cluster = self.clusters.pop(0)
        return self.active_cluster

    def get_active_cluster(self):
        return self.active_cluster

    def get_number_of_clusters(self):
        return len(self.clusters)

    def add_target(self, coordinates, color=WHITE_COLOR):
        self.active_cluster.add_target(coordinates)
        self.visualizer.add_sphere(coordinates, color)

    def remove_target(self, coordinates):
        self.active_cluster.remove_target(coordinates)
        self.visualizer.remove_sphere(coordinates)

    def mark_target(self, coordinates, state):
        if state == "visited":
            self.visualizer.mark_sphere(coordinates, ORANGE_COLOR)
        elif state == "picked":
            self.visualizer.mark_sphere(coordinates, GREEN_COLOR)
        else:
            self.visualizer.mark_sphere(coordinates, RED_COLOR)

    def mark_cluster(self, x_start, z_start):
        self.visualizer.mark_bounding_box(x_start, z_start)

    def unmark_cluster(self, x_start, z_start):
        self.visualizer.unmark_bounding_box(x_start, z_start)

    def remove_bounding_box(self, x_start, z_start):
        self.visualizer.remove_bounding_box(x_start, z_start)


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