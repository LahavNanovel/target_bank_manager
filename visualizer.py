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
        self.axis = o3d.geometry.TriangleMesh.create_coordinate_frame(size=500, origin=[0, 0, 0])
        self.vis.add_geometry(self.axis)
        while self.is_active:
            while not self.display_requests.empty():
                self.vis.add_geometry(self.axis)
                self.vis.poll_events()
                self.vis.update_renderer()
                self.displayed_geometries.append(self.display_requests.get())
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
        for c in coordinates:
            sphere = Sphere(c[0], c[1], c[2], color, ORANGE_RADIUS)
            self.add_element(sphere.get_mesh_sphere())

    def set_path(self, order):
        for i in range(len(order) - 1):
            self.add_line(order[i], order[i + 1])

    def set_bounding_box(self, x_start, z_start, t_min, t_max):
        window_width = RS_WIDTH
        window_height = RS_HEIGHT
        edge = ORANGE_RADIUS
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

    def add_element(self, element):
        self.display_requests.put(element)

    def add_line(self, source, destination, color=BLACK_COLOR):
        line_set = o3d.geometry.LineSet()
        line_set.points = o3d.utility.Vector3dVector([source, destination])
        line_set.lines = o3d.utility.Vector2iVector([[0, 1]])
        line_set.colors = o3d.utility.Vector3dVector([color])
        # print(line_set.get_line_coordinate(0))
        self.add_element(line_set)

    def load_viewpoint(self):
        ctr = self.vis.get_view_control()
        param = o3d.io.read_pinhole_camera_parameters('viewpoint.json')
        ctr.convert_from_pinhole_camera_parameters(param)

    def save_viewpoint(self):
        param = self.vis.get_view_control().convert_to_pinhole_camera_parameters()
        o3d.io.write_pinhole_camera_parameters('viewpoint.json', param)
        # self.vis.destroy_window()

    def mark_sphere(self, coordinates, color):
        z = coordinates[0]
        x = coordinates[1]
        t = coordinates[2]
        geometry = self.get_sphere_by_coordinates(z, x, t)
        geometry.paint_uniform_color(color)
        self.vis.update_geometry(geometry)

    def get_sphere_by_coordinates(self, z, x, t):
        for element in self.displayed_geometries:
            center = element.get_center()
            if abs(z - center[1]) < 0.0001 and abs(x - center[0]) < 0.0001 and abs(t - center[2]) < 0.0001:
                return element
        return None

    def get_line_by_coordinates(self, z, x, t):
        for element in self.displayed_geometries:
            print(element.get_line_coordinate(0))

    def add_sphere(self, coordinates, color):
        sphere = Sphere(coordinates[0], coordinates[1], coordinates[2], color, ORANGE_RADIUS)
        self.add_element(sphere.get_mesh_sphere())

    def remove_sphere(self, coordinates):
        sphere = self.get_sphere_by_coordinates(coordinates[0], coordinates[1], coordinates[2])
        self.displayed_geometries.remove(sphere)
        self.vis.remove_geometry(sphere)
        self.vis.update_geometry(sphere)