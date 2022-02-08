import time
import threading

from point_generator_for_debug import generate_points
from target_bank_manager import getTargetBankManager

range_1 = [[100, 200], [200, 400]]
range_2 = [[650, 750], [100, 300]]
range_3 = [[400, 500], [600, 800]]
range_4 = [[250, 350], [900, 1100]]

ranges = {}
ranges["z_axis_range"] = -2000, 5000
ranges["x_axis_range"] = -2000, 5000
ranges["t_axis_range"] = 0, 5000

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
    targets = targets_1 + targets_2 + targets_3 + targets_4
    getTargetBankManager().set_targets(targets)
    targets_1 = sorted(targets_1, key=lambda k: [k[2]])
    targets_2 = sorted(targets_2, key=lambda k: [k[2]])
    targets_3 = sorted(targets_3, key=lambda k: [k[2]])
    targets_4 = sorted(targets_4, key=lambda k: [k[2]])
    time.sleep(5)
    getTargetBankManager().mark_orange(targets_1[0], "visited")
    time.sleep(2)
    getTargetBankManager().mark_orange(targets_1[0], "picked")
    time.sleep(2)
    getTargetBankManager().mark_orange(targets_1[1], "visited")
    time.sleep(2)
    getTargetBankManager().mark_orange(targets_1[1], "failed")
    time.sleep(2)
    getTargetBankManager().mark_orange(targets_2[0], "visited")
    time.sleep(2)
    getTargetBankManager().mark_orange(targets_2[0], "picked")
    time.sleep(2)
    getTargetBankManager().mark_orange(targets_3[0], "visited")
    time.sleep(2)
    getTargetBankManager().mark_orange(targets_3[0], "picked")
    time.sleep(2)
    getTargetBankManager().mark_orange(targets_4[0], "visited")
    time.sleep(2)
    getTargetBankManager().mark_orange(targets_4[0], "picked")



if __name__ == "__main__":
    getTargetBankManager().set_motor_range(ranges)
    insert_thread = threading.Thread(target=test_2)
    insert_thread.run()
