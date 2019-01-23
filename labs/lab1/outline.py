from typing import List, Tuple

from numpy import array
from OpenGL import GL

from lab1.utils import draw_bezier_curve, transform_point

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

    @classmethod
    def get_by_points(cls, points: PointsList, helper_points: PointsList):
        for i in range(len(points)):
            points[i] = tuple(transform_point(point) for point in points[i])

        for i in range(len(helper_points)):
            helper_points[i] = tuple(transform_point(point) for point in helper_points[i])

        sections = []
        for (p1, p4), (p2, p3) in zip(points, helper_points):
            sections.append((
                array(p1),
                array(p2),
                array(p3),
                array(p4),
            ))

        return cls(sections)
