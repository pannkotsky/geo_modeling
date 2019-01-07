from numpy import array

from helpers import draw_line
from lab0.polygon import Polygon


def draw_point(point: array):
    draw_line(point + (-3, -3), point + (3, 3))
    draw_line(point + (-3, 3), point + (3, -3))


def get_object(origin):
    p0 = array((origin[0], origin[1]))
    p1 = p0 + (70, 0)
    p2 = p1 + (-10, 20)
    p3 = p2 + (-50, 0)
    p4 = p3 + (5, 0)
    p5 = p4 + (0, 55)
    p6 = p5 + (40, 0)
    p7 = p6 + (0, -55)
    p8 = p4 + (5, 0)
    p9 = p8 + (0, 40)
    p10 = p9 + (30, 0)
    p11 = p10 + (0, -40)

    edges = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11]
    sides = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (8, 9),
        (9, 10),
        (10, 11),
    ]

    return Polygon(edges, sides)
