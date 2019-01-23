from copy import deepcopy
from itertools import tee
from typing import Iterable, Tuple

from numpy import array

from helpers import draw_line


def bezier_3(u: float, a: array, b: array, c: array, d: array):
    def calc_coord(i):
        return (
            a[i] * (1 - u) ** 3 +
            3 * b[i] * u * (1 - u) ** 2 +
            3 * c[i] * u ** 2 * (1 - u) +
            d[i] * u ** 3
        )

    return array([calc_coord(i) for i in range(2)])


def pairwise(iterable: Iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def get_bezier_curve(a: array, b: array, c: array, d: array):
    return (bezier_3(u / 100, a, b, c, d) for u in range(101))


def draw_bezier_curve(a: array, b: array, c: array, d: array):
    for p0, p1 in pairwise(get_bezier_curve(a, b, c, d)):
        draw_line(p0, p1)


def transform_point(point: Tuple[int, int], height: int, shift_x: int, shift_y: int) -> Tuple[int, int]:
    x, y = point
    return x // 2 + shift_x, height - y // 2 + shift_y
