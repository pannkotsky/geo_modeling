from numpy import array

from lab0.polygon import Polygon


class Point(Polygon):
    def __init__(self, point: array, radius: int = 3):
        edges = [
            point + (-radius, -radius),
            point + (radius, radius),
            point + (-radius, radius),
            point + (radius, -radius),
        ]
        sides = [
            (0, 1),
            (2, 3),
        ]
        super().__init__(edges, sides, line_width=1)
        self.point = point
