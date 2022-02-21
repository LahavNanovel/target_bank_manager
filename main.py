import time
import threading
from constants import *
from point_generator_for_debug import *
from target_bank_manager import getTargetBankManager

range_1 = [[650, 750], [100, 300]]
range_2 = [[100, 200], [200, 400]]
range_3 = [[400, 500], [600, 800]]
range_4 = [[250, 350], [900, 1100]]

ranges = {}
ranges["z_axis_range"] = 0, 1800
ranges["x_axis_range"] = 0, 1000
ranges["t_axis_range"] = 0, 2000


# mark bounding boxes and targets
def test_1():
    targets = generate_points_from_file()
    getTargetBankManager().set_targets(targets)
    num_clusters = getTargetBankManager().get_number_of_clusters()
    time.sleep(2)
    for i in range (num_clusters):
        cluster = getTargetBankManager().get_next_cluster()
        x_start = cluster.get_x_start()
        z_start = cluster.get_z_start()
        getTargetBankManager().mark_cluster(x_start, z_start)
        time.sleep(2)
        targets = cluster.get_target_list()
        if i == 1:
            getTargetBankManager().mark_target(targets[0], "visited")
            time.sleep(2)
            getTargetBankManager().mark_target(targets[0], "failed")
            time.sleep(2)
        else:
            getTargetBankManager().mark_target(targets[0], "visited")
            time.sleep(2)
            getTargetBankManager().mark_target(targets[0], "picked")
            time.sleep(2)
        getTargetBankManager().unmark_cluster(x_start, z_start)
        time.sleep(2)

# add and remove
def test_2():
    targets_1 = generate_points([range_1])
    getTargetBankManager().set_targets(targets_1)
    cluster = getTargetBankManager().get_next_cluster()
    time.sleep(2)
    getTargetBankManager().add_target([200, 400, 500])
    time.sleep(2)
    getTargetBankManager().remove_target([200, 400, 500])
    time.sleep(2)
    getTargetBankManager().remove_bounding_box(cluster.get_x_start(), cluster.get_z_start())

if __name__ == "__main__":
    getTargetBankManager().set_motor_range(ranges)
    t = threading.Thread(target=test_1)
    t.run()
