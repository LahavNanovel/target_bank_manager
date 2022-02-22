import time
from visualizer import Visualizer

if __name__ == "__main__":
    visualizer = Visualizer()
    sphere_dict_1 = {
        "z_value": 100,
        "x_value": 100,
        "t_value": 100
    }
    visualizer.add_sphere_from_dict(sphere_dict_1)
    time.sleep(1)
    sphere_dict_2 = {
        "z_value": 200,
        "x_value": 200,
        "t_value": 200
    }
    visualizer.add_sphere_from_dict(sphere_dict_2)