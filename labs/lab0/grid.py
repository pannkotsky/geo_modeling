from copy import deepcopy
from itertools import chain

from numpy import array
from OpenGL import GL

from helpers import affinate_point, draw_line, draw_text, project_point


class Grid:
    def __init__(self, origin: array, width: int, height: int, division: int):
        self.origin = origin

        x, y = origin

        self.x_axis = [
            origin,
            array((x + width, y))
        ]
        self.y_axis = [
            origin,
            array((x, y + height))
        ]

        self.horizontal_grid = []
        while y <= origin[1] + height - division:
            y += division
            self.horizontal_grid.append(
                [
                    array((x, y)),
                    array((x + width, y))
                ]
            )

        y = origin[1]
        self.vertical_grid = []
        while x <= origin[0] + width - division:
            x += division
            self.vertical_grid.append(
                [
                    array((x, y)),
                    array((x, y + height))
                ]
            )

        self.mark = self.origin + (division, 0)
        self.affination = None

    def draw(self):
        GL.glColor3f(0.25, 0.25, 0.25)
        draw_line(*self.x_axis)
        draw_line(*self.y_axis)

        GL.glColor3f(0.75, 0.75, 0.75)
        for line in chain(self.horizontal_grid, self.vertical_grid):
            draw_line(*line)

        GL.glColor3f(0.25, 0.25, 0.25)
        GL.glLineWidth(2)
        draw_line(self.mark + (0, 5), self.mark + (0, -5))
        GL.glLineWidth(1)

        draw_text(self.origin + (2, -10), "0")
        draw_text(self.mark + (2, -10), "20")
        draw_text(self.x_axis[1] + (2, -10), "X")
        draw_text(self.y_axis[1] + (2, -10), "Y")

    def affinate(self, direction_x: array, direction_y: array):
        origin = self.origin
        self.x_axis = [affinate_point(p, direction_x, direction_y, origin) for p in self.x_axis]
        self.y_axis = [affinate_point(p, direction_x, direction_y, origin) for p in self.y_axis]

        for i in range(len(self.horizontal_grid)):
            self.horizontal_grid[i] = [affinate_point(p, direction_x, direction_y, origin)
                                       for p in self.horizontal_grid[i]]

        for i in range(len(self.vertical_grid)):
            self.vertical_grid[i] = [affinate_point(p, direction_x, direction_y, origin)
                                     for p in self.vertical_grid[i]]

        self.mark = affinate_point(self.mark, direction_x, direction_y, origin)

    def project(self, x_end: array, x_weight: float, y_end: array, y_weight: float,
                origin_weight: float, origin: array):
        self.x_axis = [project_point(p, x_end, x_weight, y_end, y_weight, origin_weight, origin)
                       for p in self.x_axis]
        self.y_axis = [project_point(p, x_end, x_weight, y_end, y_weight, origin_weight, origin)
                       for p in self.y_axis]

        for i in range(len(self.horizontal_grid)):
            self.horizontal_grid[i] = [project_point(p, x_end, x_weight, y_end, y_weight,
                                                     origin_weight, origin)
                                       for p in self.horizontal_grid[i]]

        for i in range(len(self.vertical_grid)):
            self.vertical_grid[i] = [project_point(p, x_end, x_weight, y_end, y_weight,
                                                   origin_weight, origin)
                                     for p in self.vertical_grid[i]]

        self.mark = project_point(self.mark, x_end, x_weight, y_end, y_weight, origin_weight,
                                  origin)
