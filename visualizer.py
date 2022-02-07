import time
import math
import queue
import threading
import open3d as o3d
from constants import *


class Sphere:
    def __init__(self, z, x, t, color, radius):
        self.zPos   = z
        self.xPos   = x
        self.tPos   = t
        self.radius = radius
        self.color  = color
        self.mesh_sphere = self.create_mesh_sphere()

    def get_x(self):
        return self.xPos

    def get_z(self):
        return self.zPos

    def get_t(self):
        return self.tPos

    def calculate_distance(self, other):
        d1 = pow(self.xPos - other.get_x(), 2)
        d2 = pow(self.zPos - other.get_z(), 2)
        d3 = pow(self.tPos - other.get_t(), 2)
        return math.sqrt(d1 + d2 + d3)

    def create_mesh_sphere(self):
        mesh_sphere = o3d.geometry.TriangleMesh.create_sphere(radius=self.radius)
        mesh_sphere.compute_vertex_normals()
        mesh_sphere.translate([self.xPos, self.zPos, self.tPos])
        mesh_sphere.paint_uniform_color(self.color)
        return mesh_sphere

    def get_mesh_sphere(self):
        return self.mesh_sphere


class Visualizer:
    colors = [ORANGE_COLOR, GREEN_COLOR, YELLOW_COLOR, RED_COLOR, PURPLE_COLOR, BLUE_COLOR, BLACK_COLOR]

    def __init__(self):
        self.displayed_geometries = []
        self.display_requests = queue.Queue()
        self.is_active = True
        self.activation_thread = threading.Thread(target=self.create_window)
        self.activation_thread.start()

    def create_window(self):
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window(window_name="x: red | z: green | t: blue")
        axis = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.08, origin=[0, 0, 0])
        self.add_element(axis)
        while self.is_active:
            while not self.display_requests.empty():
                self.vis.clear_geometries()
                geometry = self.display_requests.get()
                self.displayed_geometries.append(geometry)
                for geometry in self.displayed_geometries:
                    self.vis.add_geometry(geometry)
                    self.vis.update_geometry(geometry)
            self.vis.poll_events()
            self.vis.update_renderer()
        self.vis.destroy_window()

    def set_spheres(self, coordinates, color=ORANGE_COLOR):
        for c in coordinates:
            # check if coordinates are in axis range.
            if not self.is_point_in_range(c[0]) or not self.is_point_in_range(c[1]) or not self.is_point_in_range(c[2]):
                continue
            # normalize coordinates.
            sphere = Sphere(c[0] / self.z_ref, c[1] / self.x_ref, c[2] / self.t_ref, color, ORANGE_RADIUS / self.x_ref)
            self.add_element(sphere.get_mesh_sphere())

    def set_path(self, order):
        normalized_order = []
        for point in order:
            normalized_order.append([point[1] / self.z_ref, point[0] / self.x_ref, point[2] / self.t_ref])
        for i in range(len(normalized_order) - 1):
            self.add_line(normalized_order[i], normalized_order[i + 1])

    def set_ref(self, z_ref, x_ref, t_ref):
        self.z_ref = z_ref
        self.x_ref = x_ref
        self.t_ref = t_ref

    def is_point_in_range(self, point):
        if point < -2000 or point > 5000:
            return False
        return True

    def add_element(self, element):
        self.display_requests.put(element)

    def add_line(self, source, destination, color=BLACK_COLOR):
        line_set = o3d.geometry.LineSet()
        line_set.points = o3d.utility.Vector3dVector([source, destination])
        line_set.lines = o3d.utility.Vector2iVector([[0, 1]])
        line_set.colors = o3d.utility.Vector3dVector([color])
        self.add_element(line_set)

    def load_viewpoint(self):
        ctr = self.vis.get_view_control()
        param = o3d.io.read_pinhole_camera_parameters('viewpoint.json')
        ctr.convert_from_pinhole_camera_parameters(param)

    def save_viewpoint(self):
        param = self.vis.get_view_control().convert_to_pinhole_camera_parameters()
        o3d.io.write_pinhole_camera_parameters('viewpoint.json', param)
        # self.vis.destroy_window()

