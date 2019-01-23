from typing import List, Tuple

from numpy import array
from OpenGL import GL

from lab1.utils import draw_bezier_curve

Section = Tuple[array, array, array, array]
PointsList = List[
    Tuple[
        Tuple[int, int],
        Tuple[int, int]
    ]
]
Color = Tuple[float, float, float]

BLACK = (0, 0, 0)
HEIGHT = 604
PADDING = 20


class Outline:
    def __init__(self, sections: List[Section], line_width: int=2, color: Color=BLACK):
        self.sections = sections
        self.line_width = line_width
        self.color = color

    def draw(self):
        GL.glLineWidth(self.line_width)
        GL.glColor3f(*self.color)

        for section in self.sections:
            draw_bezier_curve(*section)

        GL.glLineWidth(1)

    def intermediate(self, other, total_steps, step):
        sections = []
        portion = step / total_steps
        for section1, section2 in zip(self.sections, other.sections):
            intermediate_points = tuple(point1 + (point2 - point1) * portion for point1, point2 in zip(section1, section2))
            sections.append(intermediate_points)

        return self.__class__(sections)
