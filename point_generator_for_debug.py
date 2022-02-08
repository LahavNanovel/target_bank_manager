import random

def generate_points(ranges):
    targets = []
    for r in ranges:
        for i in range (4):
            x_start = r[0][0]
            x_end = r[0][1]
            z_start = r[1][0]
            z_end = r[1][1]
            x = float(random.randint(x_start, x_end))
            z = float(random.randint(z_start, z_end))
            t = float(random.randint(0, 500))
            targets.append([z, x, t])
    return targets