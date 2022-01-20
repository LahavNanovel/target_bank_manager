from constants import *
from cluster_creator import ClusterCreator
from path_solver import PathSolver
from visualizer import Visualizer
# from cameras.camerasOffset.camerasOffset import getCamerasOffset, CamerasOffset

class TargetBankManager:
    def __init__(self):
        self.cluster_creator = ClusterCreator(x_start=0, z_start=0,
                                              width=REF, height=REF,
                                              window_width=RS_WIDTH, window_height=RS_HEIGHT,
                                              shift_size=SHIFT_SIZE)
        self.path_solver = PathSolver()
        self.visualizer = Visualizer()
        self.clusters = []

    def set_motor_range(self, range_dictionary: dict):
        self.x_start, self.x_end = range_dictionary["x_axis_range"]
        self.z_start, self.z_end = range_dictionary["z_axis_range"]
        self.t_start, self.t_end = range_dictionary["t_axis_range"]

    def is_point_in_range(self, point, x_offset, z_offset, t_offset):
        if (point[0] + x_offset) < self.x_start or (point[0] + x_offset) > self.x_end:
            return False
        if (point[1] + z_offset) < self.z_start or (point[1] + z_offset) > self.z_end:
            return False
        if (point[2] + t_offset) < self.t_start or (point[2] + t_offset) > self.t_end:
            return False
        return True

    def filter_out_of_range_points(self, points):
        # in_range = []
        # for point in points:
        #     getCamerasOffset().load_init_data()  # reload the data from the file
        #     x_offset = getCamerasOffset().get_offset(key_cam_offset=CamerasOffset.REMOTE_CAM_X_OFFSET)
        #     z_offset = getCamerasOffset().get_offset(key_cam_offset=CamerasOffset.REMOTE_CAM_Z_OFFSET)
        #     t_offset = getCamerasOffset().get_offset(key_cam_offset=CamerasOffset.REMOTE_CAM_T_OFFSET)
        #     if self.is_point_in_range(point, x_offset, z_offset, t_offset):
        #         in_range.append(point)
        # return in_range
        pass

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

    def get_next_cluster(self):
        pass

    def get_number_of_clusters(self):
        pass


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