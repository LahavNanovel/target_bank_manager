import time
import threading

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

# mark targets.
def test_1():
    targets_1 = generate_points([range_1])
    targets_2 = generate_points([range_2])
    targets_3 = generate_points([range_3])
    targets_4 = generate_points([range_4])
    targets_1 = sorted(targets_1, key=lambda k: [k[2]])
    targets_2 = sorted(targets_2, key=lambda k: [k[2]])
    targets_3 = sorted(targets_3, key=lambda k: [k[2]])
    targets_4 = sorted(targets_4, key=lambda k: [k[2]])
    targets = targets_1 + targets_2 + targets_3 + targets_4
    getTargetBankManager().set_targets(targets)
    time.sleep(10)
    getTargetBankManager().mark_target(targets_1[0], "visited")
    time.sleep(3)
    getTargetBankManager().mark_target(targets_1[0], "picked")
    time.sleep(3)
    getTargetBankManager().mark_target(targets_1[1], "visited")
    time.sleep(3)
    getTargetBankManager().mark_target(targets_1[1], "failed")
    time.sleep(3)
    getTargetBankManager().mark_target(targets_2[0], "visited")
    time.sleep(3)
    getTargetBankManager().mark_target(targets_2[0], "picked")
    time.sleep(3)
    getTargetBankManager().mark_target(targets_2[1], "visited")
    time.sleep(3)
    getTargetBankManager().mark_target(targets_2[1], "picked")
    time.sleep(3)
    getTargetBankManager().mark_target(targets_3[0], "visited")
    time.sleep(3)
    getTargetBankManager().mark_target(targets_3[0], "picked")
    time.sleep(3)
    getTargetBankManager().mark_target(targets_3[1], "visited")
    time.sleep(3)
    getTargetBankManager().mark_target(targets_3[1], "failed")
    time.sleep(3)
    getTargetBankManager().mark_target(targets_4[0], "visited")
    time.sleep(3)
    getTargetBankManager().mark_target(targets_4[0], "picked")
    time.sleep(3)
    getTargetBankManager().mark_target(targets_4[1], "visited")
    time.sleep(3)
    getTargetBankManager().mark_target(targets_4[1], "picked")

# mark bounding box
def test_2():
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
        getTargetBankManager().unmark_cluster(x_start, z_start)
        time.sleep(2)

# add and remove spheres
def test_3():
    targets_1 = generate_points([range_1])
    getTargetBankManager().set_targets(targets_1)
    cluster = getTargetBankManager().get_next_cluster()
    time.sleep(2)
    getTargetBankManager().add_target([200, 400, 500])
    time.sleep(2)
    getTargetBankManager().remove_target([200, 400, 500])

# generate points from real detection file
def test_4():
    targets = generate_points_from_file()
    getTargetBankManager().set_targets(targets)


if __name__ == "__main__":
    getTargetBankManager().set_motor_range(ranges)
    t = threading.Thread(target=test_2)
    t.run()
