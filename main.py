from point_generator import generate_points
from target_bank_manager import getTargetBankManager

range_1 = [[100, 200], [200, 400]]
range_2 = [[650, 750], [100, 300]]
range_3 = [[400, 500], [600, 800]]
range_4 = [[250, 350], [900, 1100]]
ranges = [range_1, range_2, range_3, range_4]

if __name__ == "__main__":
    targets = generate_points(ranges)
    getTargetBankManager().update_targets(targets)
    getTargetBankManager().visualize()
