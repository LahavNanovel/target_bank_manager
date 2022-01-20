from point_generator import generate_points
from target_bank_manager import getTargetBankManager

range_1 = [[100, 200], [200, 400]]
range_2 = [[650, 750], [100, 300]]
range_3 = [[400, 500], [600, 800]]
range_4 = [[250, 350], [900, 1100]]

if __name__ == "__main__":
    targets_1 = generate_points([range_1, range_2])
    getTargetBankManager().update_targets(targets_1)

    targets_2 = generate_points([range_3, range_4])
    getTargetBankManager().update_targets(targets_2)

    getTargetBankManager().visualize()
