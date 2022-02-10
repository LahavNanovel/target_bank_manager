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
ranges["x_axis_range"] = 0, 895
ranges["t_axis_range"] = 0, 2000

# add clusters gradually
def test_1():
    targets_1 = generate_points([range_1])
    getTargetBankManager().set_targets(targets_1)
    time.sleep(2)
    targets_2 = generate_points([range_1, range_2])
    getTargetBankManager().set_targets(targets_2)
    time.sleep(2)
    targets_3 = generate_points([range_1, range_2, range_3])
    getTargetBankManager().set_targets(targets_3)
    time.sleep(2)
    targets_4 = generate_points([range_1, range_2, range_3, range_4])
    getTargetBankManager().set_targets(targets_4)

# add clusters at once and mark targets.
def test_2():
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

# generate points from real detection file
def test_3():
    targets = generate_points_from_file()
    getTargetBankManager().set_targets(targets)

if __name__ == "__main__":
    getTargetBankManager().set_motor_range(ranges)
    t = threading.Thread(target=test_3)
    t.run()
