from typing import Tuple, List

from numpy import array
from OpenGL import GL

from helpers import draw_line, rotate_point
from lab0.figure import Figure

Side = Tuple[int, int]
Color = Tuple[int, int, int]

BLACK = (0, 0, 0)


class Polygon(Figure):
    def __init__(self, edges: List[array], sides: List[Side], line_width: int = 2,
                 color: Color = BLACK):
        super().__init__()
        self.edges = edges
        self.sides = sides
        self.line_width = line_width
        self.color = color

    def _draw(self):
        GL.glLineWidth(self.line_width)
        GL.glColor3f(*self.color)

        for side in self.sides:
            draw_line(self.edges[side[0]], self.edges[side[1]])

        GL.glLineWidth(1)

    def shift(self, shift_x: int, shift_y: int):
        for i in range(len(self.edges)):
            self.edges[i] += (shift_x, shift_y)

    def rotate(self, rot_point: array, rot_angle: int):
        for i in range(len(self.edges)):
            self.edges[i] = rotate_point(self.edges[i], rot_point, rot_angle)

    def _transform(self, transform_fn):
        for i in range(len(self.edges)):
            self.edges[i] = transform_fn(self.edges[i])
