from numpy import array
from OpenGL import GL

from helpers import draw_line, draw_text
from lab0.polygon import Polygon


def draw_grid(origin: array, width: int, height: int, division: int):
    x = origin[0]
    y = origin[1]

    half_width = width // 2
    half_height = height // 2

    GL.glColor3f(0.25, 0.25, 0.25)

    # x axis
    draw_line((x - half_width, y), (x + half_width, y))
    # y axis
    draw_line((x, y - half_height), (x, y + half_height))

    GL.glColor3f(0.75, 0.75, 0.75)

    # horizontal grid
    while y <= origin[1] + half_height - division:
        y += division
        draw_line((x - half_width, y), (x + half_width, y))

    y = origin[1]
    while y >= origin[1] - half_height + division:
        y -= division
        draw_line((x - half_width, y), (x + half_width, y))

    y = origin[1]
    # vertical grid
    while x <= origin[0] + half_width - division:
        x += division
        draw_line((x, y - half_height), (x, y + half_height))

    x = origin[0]
    while x >= origin[0] - half_width + division:
        x -= division
        draw_line((x, y - half_height), (x, y + half_height))

    GL.glColor3f(0.25, 0.25, 0.25)
    GL.glLineWidth(2)
    draw_line(origin + (20, 5), origin + (20, -5))
    GL.glLineWidth(1)

    draw_text(origin + (2, -10), "0")
    draw_text(origin + (22, -10), "20")
    draw_text(origin + (half_width + 2, -10), "X")
    draw_text(origin + (2, half_height - 10), "Y")


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
