import time
import math
import threading
import open3d as o3d
from constants import *


class Sphere:
    def __init__(self, x, z, t, color, radius):
        self.xPos   = x
        self.zPos   = z
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
        self.spheres = []
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window(window_name="x: red | z: green | t: blue")
        # activate window in another thread and wait for signal (after update is finished) to hit window.run()
        self.e = threading.Event()
        self.activation_thread = threading.Thread(target=self.activate_window)
        self.activation_thread.start()

    def import_spheres_from_array(self, coordinates, color=ORANGE_COLOR):
        for c in coordinates:
            # check if coordinates are in range [-2000, 5000]
            if not self.is_point_in_range(c[0]) or not self.is_point_in_range(c[1]) or not self.is_point_in_range(c[2]):
                continue
            # normalize coordinates
            sphere = Sphere(c[1] / self.z_ref, c[0] / self.x_ref, c[2] / self.t_ref, color, ORANGE_RADIUS / self.x_ref)
            self.spheres.append(sphere)

    def import_spheres_from_file(self, file_path, color=ORANGE_COLOR):
        f = open(file_path, 'r')
        lines = f.readlines()
        for line in lines:
            c = line.split(" ")
            c = [int(float(element)) for element in c]
            # check if coordinates are in range [-2000, 5000]
            if not self.is_point_in_range(c[0]) or not self.is_point_in_range(c[1]) or not self.is_point_in_range(c[2]):
                continue
            # normalize coordinates
            sphere = Sphere(c[1] / self.z_ref, c[0] / self.x_ref, c[2] / self.t_ref, color, ORANGE_RADIUS / self.x_ref)
            self.spheres.append(sphere)

    def import_path_from_array(self, order):
        self.order = []
        for point in order:
            self.order.append([point[1] / self.z_ref, point[0] / self.x_ref, point[2] / self.t_ref])

    def is_point_in_range(self, point):
        if point < -2000 or point > 5000:
            return False
        return True

    def add_element(self, element):
        self.vis.add_geometry(element)
        self.vis.update_geometry(element)
        self.vis.update_renderer()
        self.vis.poll_events()

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
        self.vis.destroy_window()

    def activate_window(self):  
        # waits until a signal is given
        self.e.wait()
        self.load_viewpoint()
        # before vis.run() it's not possible to change the display,
        # after vis.run() it's not possible to update the viewed elements
        self.vis.run()
        self.vis.destroy_window()
        # uncomment to save new viewpoint
        self.save_viewpoint()

    def finished_updating(self):
        # draw the coordinate axis.
        axis = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.08, origin=[0, 0, 0])
        self.add_element(axis)
        # draw all spheres
        for sphere in self.spheres:
            self.add_element(sphere.get_mesh_sphere())
        # draw all lines of path.
        for i in range (len(self.order) - 1):
            self.add_line(self.order[i], self.order[i + 1])
            time.sleep(0.15)
        # release the activate thread event to run the visualizer 
        # this operation will cause blocking of the main thread (meaning that updates will no longer be possible)
        self.e.set()

    def set_ref(self, z_ref, x_ref, t_ref):
        self.z_ref = z_ref
        self.x_ref = x_ref
        self.t_ref = t_ref

    # def add_element(self, element):
    #     self.activation_thread = threading.Thread(target=self.activate_add_element, args=[element])
    #     self.activation_thread.start()
    #
    # def add_line(self, element):
    #     self.activation_thread = threading.Thread(target=self.activate_add_line, args=[element])
    #     self.activation_thread.start()
