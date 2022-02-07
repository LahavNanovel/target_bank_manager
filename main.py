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

def insert_targets():
    targets_1 = generate_points([range_1])
    getTargetBankManager().update_targets(targets_1)
    time.sleep(1)
    targets_2 = generate_points([range_1, range_2])
    getTargetBankManager().update_targets(targets_2)
    time.sleep(1)
    targets_3 = generate_points([range_1, range_2, range_3])
    getTargetBankManager().update_targets(targets_3)
    time.sleep(1)
    targets_4 = generate_points([range_1, range_2, range_3, range_4])
    getTargetBankManager().update_targets(targets_4)


if __name__ == "__main__":
    getTargetBankManager().set_motor_range(ranges)
    insert_thread = threading.Thread(target=insert_targets)
    insert_thread.run()
