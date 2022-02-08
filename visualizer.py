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
    def __init__(self):
        self.displayed_geometries = []
        self.display_requests = queue.Queue()
        self.is_active = True
        self.activation_thread = threading.Thread(target=self.create_window)
        self.activation_thread.start()

    def create_window(self):
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window(window_name="x: red | z: green | t: blue")
        self.axis = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.08, origin=[0, 0, 0])
        self.vis.add_geometry(self.axis)
        while self.is_active:
            while not self.display_requests.empty():
                self.vis.clear_geometries()
                self.vis.add_geometry(self.axis)
                self.vis.poll_events()
                self.vis.update_renderer()
                geometry = self.display_requests.get()
                self.displayed_geometries.append(geometry)
                self.vis.poll_events()
                self.vis.update_renderer()
                for geometry in self.displayed_geometries:
                    self.vis.add_geometry(geometry)
            self.vis.poll_events()
            self.vis.update_renderer()
        self.vis.destroy_window()

    def clear(self):
        self.displayed_geometries = []
        self.vis.clear_geometries()
        self.vis.add_geometry(self.axis)

    def set_spheres(self, coordinates, color=ORANGE_COLOR):
        self.clear()
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

    def set_bounding_box(self, x_start, z_start, t_min, t_max):
        x_start = x_start / self.x_ref
        z_start = z_start / self.z_ref
        t_min = t_min / self.t_ref
        t_max = t_max / self.t_ref
        window_width = RS_WIDTH / self.x_ref
        window_height = RS_HEIGHT / self.z_ref
        edge = ORANGE_RADIUS / self.x_ref
        # create points
        p1 = [x_start - edge, z_start - edge, t_min - edge]
        p2 = [x_start + window_width + edge, z_start - edge, t_min - edge]
        p3 = [x_start - edge, z_start + window_height + edge, t_min - edge]
        p4 = [x_start + window_width + edge, z_start + window_height + edge, t_min - edge]
        p5 = [x_start - edge, z_start - edge, t_max+ edge]
        p6 = [x_start + window_width + edge, z_start - edge, t_max + edge]
        p7 = [x_start - edge, z_start + window_height + edge, t_max+ edge]
        p8 = [x_start + window_width + edge, z_start + window_height + edge, t_max+ edge]
        # connect points by lines
        self.add_line(p1, p2)
        self.add_line(p2, p4)
        self.add_line(p4, p3)
        self.add_line(p3, p1)
        self.add_line(p5, p6)
        self.add_line(p6, p8)
        self.add_line(p8, p7)
        self.add_line(p7, p5)
        self.add_line(p1, p5)
        self.add_line(p2, p6)
        self.add_line(p3, p7)
        self.add_line(p4, p8)

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

    def get_sphere_by_coordinates(self, z, x, t):
        for element in self.displayed_geometries:
            center = element.get_center()
            if abs(z - center[1]) < 0.0001 and abs(x - center[0]) < 0.0001 and abs(t - center[2]) < 0.0001:
                return element
        return None

    def mark_sphere(self, coordinates, color):
        z = coordinates[0] / self.z_ref
        x = coordinates[1] / self.x_ref
        t = coordinates[2] / self.t_ref
        geometry = self.get_sphere_by_coordinates(z, x, t)
        geometry.paint_uniform_color(color)
        self.vis.update_geometry(geometry)
