from copy import deepcopy

from numpy import array

from helpers import affinate_point, project_point


class Figure:
    def __init__(self):
        self.affination = None
        self.projection = None

    def _draw(self):
        raise NotImplementedError

    def draw(self):
        self.affinated().projected()._draw()

    def _transform(self, transform_fn):
        raise NotImplementedError

    def affinated(self):
        if not self.affination:
            return self

        _self = deepcopy(self)

        def transform_fn(p):
            return affinate_point(p, **_self.affination)

        _self._transform(transform_fn)
        return _self

    def affinate(self, direction_x: array, direction_y: array, origin: array):
        self.affination = {
            'direction_x': direction_x,
            'direction_y': direction_y,
            'origin': origin,
        }

    def projected(self):
        if not self.projection:
            return self

        _self = deepcopy(self)

        def transform_fn(p):
            return project_point(p, **_self.projection)

        _self._transform(transform_fn)
        return _self

    def project(self, x_end: array, x_weight: float, y_end: array, y_weight: float,
                origin_weight: float, origin: array):
        self.projection = {
            'x_end': x_end,
            'x_weight': x_weight,
            'y_end': y_end,
            'y_weight': y_weight,
            'origin_weight': origin_weight,
            'origin': origin,
        }
