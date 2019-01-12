from itertools import chain

from numpy import array
from OpenGL import GL

from helpers import draw_line, draw_text
from lab0.figure import Figure

LIGHT_GREY = (0.75, 0.75, 0.75)
DARK_GREY = (0.25, 0.25, 0.25)


class Grid(Figure):
    def __init__(self, origin: array, width: int, height: int, division: int):
        super().__init__()
        self.origin = origin

        self.x_axis = [
            origin,
            origin + (width, 0)
        ]
        self.y_axis = [
            origin,
            origin + (0, height)
        ]

        x = origin[0]
        self.horizontal_grid = []

        for y in range(origin[1], origin[1] + height + 1, division):
            self.horizontal_grid.append(
                [
                    array((x, y)),
                    array((x + width, y))
                ]
            )

        y = origin[1]
        self.vertical_grid = []

        for x in range(origin[0], origin[0] + width + 1, division):
            self.vertical_grid.append(
                [
                    array((x, y)),
                    array((x, y + height))
                ]
            )

        self.mark = self.origin + (division, 0)

    def _draw(self):
        GL.glColor3f(*DARK_GREY)
        draw_line(*self.x_axis)
        draw_line(*self.y_axis)

        GL.glColor3f(*LIGHT_GREY)
        for line in chain(self.horizontal_grid, self.vertical_grid):
            draw_line(*line)

        GL.glColor3f(*DARK_GREY)
        GL.glLineWidth(2)
        draw_line(self.mark + (0, 5), self.mark + (0, -5))
        GL.glLineWidth(1)

        draw_text(self.origin + (2, -10), "0")
        draw_text(self.mark + (2, -10), "20")
        draw_text(self.x_axis[1] + (2, -10), "X")
        draw_text(self.y_axis[1] + (2, -10), "Y")

    def _transform(self, transform_fn):
        self.x_axis = [transform_fn(p) for p in self.x_axis]
        self.y_axis = [transform_fn(p) for p in self.y_axis]

        for i in range(len(self.horizontal_grid)):
            self.horizontal_grid[i] = [transform_fn(p) for p in self.horizontal_grid[i]]

        for i in range(len(self.vertical_grid)):
            self.vertical_grid[i] = [transform_fn(p) for p in self.vertical_grid[i]]

        self.mark = transform_fn(self.mark)
