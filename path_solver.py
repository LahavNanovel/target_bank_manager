import numpy as np

class PathSolver:
    def __init__(self):
        self.coordinates = []

    def update_clusters(self, clusters):
        for cluster in clusters:
            coordinate = cluster.get_position()
            self.coordinates.append(coordinate)

    def calculate_distance(self, point1, point2):
        p1 = np.array(point1)
        p2 = np.array(point2)
        squared_dist = np.sum((p1-p2)**2, axis=0)
        return np.sqrt(squared_dist)

    def get_closest_point(self, point):
        distances = []
        for c in self.coordinates:
            distances.append(self.calculate_distance(point, c))
        # get the index of the minimum distance in list
        min_distance_index = distances.index(min(distances))
        # return the actual coordinate that the distance belongs to
        return self.coordinates[min_distance_index]

    def nearest_neighbor(self):
        order = []
        if len(self.coordinates) == 0:
            return order
        # copy the values of the coordinates
        remaining_points = self.coordinates
        # find the closest point to 0 and add it as src
        src = self.get_closest_point([0, 0, 0])
        order.append(src)
        remaining_points.remove(src)
        # loop over the coordinates to get the point which is closest to the previously added point
        while len(remaining_points) != 0:
            new_point = self.get_closest_point(order[len(order) - 1])
            order.append(new_point)
            remaining_points.remove(new_point)
        return order