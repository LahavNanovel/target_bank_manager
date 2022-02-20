import math
import queue
import threading
import open3d as o3d
from constants import *


class Sphere:
    def __init__(self, z, x, t, radius, color=WHITE_COLOR):
        self.zPos   = z
        self.xPos   = x
        self.tPos   = t
        self.radius = radius
        self.color  = color
        self.sphere_element = self.create_sphere_element()

    def calculate_distance(self, other):
        d1 = pow(self.xPos - other.get_x(), 2)
        d2 = pow(self.zPos - other.get_z(), 2)
        d3 = pow(self.tPos - other.get_t(), 2)
        return math.sqrt(d1 + d2 + d3)

    def create_sphere_element(self):
        mesh_sphere = o3d.geometry.TriangleMesh.create_sphere(radius=self.radius)
        mesh_sphere.compute_vertex_normals()
        mesh_sphere.translate([self.xPos, self.zPos, self.tPos])
        mesh_sphere.paint_uniform_color(self.color)
        return mesh_sphere

    def get_sphere_element(self):
        return self.sphere_element

    def get_x(self):
        return self.xPos

    def get_z(self):
        return self.zPos

    def get_t(self):
        return self.tPos


class Line:
    def __init__(self, source, destination, color=BLACK_COLOR):
        self.source = source
        self.destination = destination
        self.color = color
        self.line_element = self.create_line_element()

    def create_line_element(self):
        line = o3d.geometry.LineSet()
        line.points = o3d.utility.Vector3dVector([self.source, self.destination])
        line.lines = o3d.utility.Vector2iVector([[0, 1]])
        line.colors = o3d.utility.Vector3dVector([self.color])
        return line

    def get_line_element(self):
        return self.line_element


class BoundingBox:
    def __init__(self, x_start, z_start, t_min, t_max):
        self.x_start = x_start
        self.z_start = z_start
        self.t_min = t_min
        self.t_max = t_max
        self.lines = self.create_bounding_box_lines()

    def create_line(self, source, destination, color=BLACK_COLOR):
        line = o3d.geometry.LineSet()
        line.points = o3d.utility.Vector3dVector([source, destination])
        line.lines = o3d.utility.Vector2iVector([[0, 1]])
        line.colors = o3d.utility.Vector3dVector([color])
        return line

    def create_bounding_box_lines(self):
        window_width = RS_WIDTH
        window_height = RS_HEIGHT
        edge = ORANGE_RADIUS
        # create points
        p1 = [self.x_start - edge, self.z_start - edge, self.t_min - edge]
        p2 = [self.x_start + window_width + edge, self.z_start - edge, self.t_min - edge]
        p3 = [self.x_start - edge, self.z_start + window_height + edge, self.t_min - edge]
        p4 = [self.x_start + window_width + edge, self.z_start + window_height + edge, self.t_min - edge]
        p5 = [self.x_start - edge, self.z_start - edge, self.t_max+ edge]
        p6 = [self.x_start + window_width + edge, self.z_start - edge, self.t_max + edge]
        p7 = [self.x_start - edge, self.z_start + window_height + edge, self.t_max+ edge]
        p8 = [self.x_start + window_width + edge, self.z_start + window_height + edge, self.t_max+ edge]
        # create lines between points
        lines = [Line(p1, p2),
                 Line(p1, p2),
                 Line(p2, p4),
                 Line(p4, p3),
                 Line(p3, p1),
                 Line(p5, p6),
                 Line(p6, p8),
                 Line(p8, p7),
                 Line(p7, p5),
                 Line(p1, p5),
                 Line(p2, p6),
                 Line(p3, p7),
                 Line(p4, p8)]
        return lines

    def get_box_lines(self):
        return self.lines

    def get_x_start(self):
        return self.x_start

    def get_z_start(self):
        return self.z_start


class Visualizer:
    def __init__(self):
        self.is_active = True
        self.displayed_geometries = []
        self.spheres = []
        self.bounding_boxes = []
        self.display_requests = queue.Queue()
        self.activation_thread = threading.Thread(target=self.create_window)
        self.activation_thread.start()

    def create_window(self):
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window(window_name="x: red | z: green | t: blue")
        self.axis = o3d.geometry.TriangleMesh.create_coordinate_frame(size=500, origin=[0, 0, 0])
        self.vis.add_geometry(self.axis)
        while self.is_active:
            while not self.display_requests.empty():
                request = self.display_requests.get()
                self.displayed_geometries.append(request)
                self.vis.add_geometry(request)
                self.vis.poll_events()
                self.vis.update_renderer()
            self.vis.poll_events()
            self.vis.update_renderer()
        self.vis.destroy_window()

    def add_sphere(self, coordinates, color=WHITE_COLOR):
        sphere = Sphere(coordinates[0], coordinates[1], coordinates[2], ORANGE_RADIUS)
        self.spheres.append(sphere)
        self.display_requests.put(sphere.get_sphere_element())

    def remove_sphere(self, coordinates):
        spheres = self.get_spheres_by_coordinates(coordinates[0], coordinates[1], coordinates[2])
        for sphere in spheres:
            self.spheres.remove(sphere)
            self.displayed_geometries.remove(sphere.get_sphere_element())
            self.vis.remove_geometry(sphere.get_sphere_element())
            self.vis.update_geometry(sphere.get_sphere_element())

    def get_spheres_by_coordinates(self, z, x, t):
        # there might be more than one sphere with the same coordinates
        spheres = []
        for sphere in self.spheres:
            center = sphere.get_sphere_element().get_center()
            if abs(z - center[1]) < 0.0001 and abs(x - center[0]) < 0.0001 and abs(t - center[2]) < 0.0001:
                spheres.append(sphere)
        return spheres

    def mark_sphere(self, coordinates, color):
        z = coordinates[0]
        x = coordinates[1]
        t = coordinates[2]
        spheres = self.get_spheres_by_coordinates(z, x, t)
        for sphere in spheres:
            sphere_element = sphere.get_sphere_element()
            sphere_element.paint_uniform_color(color)
            self.vis.update_geometry(sphere_element)

    def add_bounding_box(self, x_start, z_start, t_min, t_max):
        bounding_box = BoundingBox(x_start, z_start, t_min, t_max)
        self.bounding_boxes.append(bounding_box)
        lines = bounding_box.get_box_lines()
        for line in lines:
            self.display_requests.put(line.get_line_element())

    def get_bounding_box_by_coordinates(self, x_start, z_start):
        for bounding_box in self.bounding_boxes:
            if x_start == bounding_box.get_x_start() and z_start == bounding_box.get_z_start():
                return bounding_box
        return None

    def mark_bounding_box(self, x_start, z_start):
        bounding_box = self.get_bounding_box_by_coordinates(x_start, z_start)
        lines = bounding_box.get_box_lines()
        for line in lines:
            line_element = line.get_line_element()
            line_element.colors = o3d.utility.Vector3dVector([RED_COLOR])
            self.vis.update_geometry(line_element)

    def unmark_bounding_box(self, x_start, z_start):
        bounding_box = self.get_bounding_box_by_coordinates(x_start, z_start)
        lines = bounding_box.get_box_lines()
        for line in lines:
            line_element = line.get_line_element()
            line_element.colors = o3d.utility.Vector3dVector([BLACK_COLOR])
            self.vis.update_geometry(line_element)

    def add_path(self, order):
        edge = ORANGE_RADIUS
        for i in range(len(order) - 1):
            p1 = [order[i][1], order[i][0], order[i][2] - edge]
            p2 = [order[i + 1][1], order[i + 1][0], order[i + 1][2] - edge]
            line = Line(p1, p2, color=GRAY_COLOR)
            self.display_requests.put(line.get_line_element())

    def load_viewpoint(self):
        ctr = self.vis.get_view_control()
        param = o3d.io.read_pinhole_camera_parameters('viewpoint.json')
        ctr.convert_from_pinhole_camera_parameters(param)

    def save_viewpoint(self):
        param = self.vis.get_view_control().convert_to_pinhole_camera_parameters()
        o3d.io.write_pinhole_camera_parameters('viewpoint.json', param)
        # self.vis.destroy_window()

    # ------------------------------------------------ drawer functions ------------------------------------------------

    def add_bounding_box_from_dict(self, bounding_box_dict):
        x_start = float(bounding_box_dict["x_start"])
        z_start = float(bounding_box_dict["z_start"])
        t_min = float(bounding_box_dict["t_min"])
        t_max = float(bounding_box_dict["t_max"])
        self.add_bounding_box(x_start, z_start, t_min, t_max)

    def add_sphere_from_dict(self, sphere_dict):
        z = float(sphere_dict["z_value"])
        x = float(sphere_dict["x_value"])
        t = float(sphere_dict["t_value"])
        self.add_sphere([z, x, t])

    def remove_sphere_from_dict(self, sphere_dict):
        z = float(sphere_dict["z_value"])
        x = float(sphere_dict["x_value"])
        t = float(sphere_dict["t_value"])
        self.remove_sphere([z, x, t])

    def add_path_from_dict(self, path_dict):
        order = path_dict["order"]
        self.add_path(order)

    def mark_sphere_from_dict(self, mark_sphere_dict):
        pass

    def mark_bounding_box_from_dict(self, mark_bounding_box_dict):
        pass

    def unmark_bounding_box_from_dict(self, unmark_bounding_box_dict):
        pass
