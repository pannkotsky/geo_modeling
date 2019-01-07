import ctypes
from math import cos, radians, sin

from numpy import array

from OpenGL import GL, GLUT


def refresh2d(width, height):
    GL.glViewport(0, 0, width, height)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GL.glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glLoadIdentity()


def draw_line(p0: array, p1: array) -> None:
    GL.glBegin(GL.GL_LINES)
    GL.glVertex2f(*p0)
    GL.glVertex2f(*p1)
    GL.glEnd()


def draw_text(origin: array, text):
    GL.glColor3f(0, 0, 0)
    GL.glRasterPos2f(*origin)

    for c in text:
        GLUT.glutBitmapCharacter(GLUT.GLUT_BITMAP_HELVETICA_10, ctypes.c_int(ord(c)))


def rotate_point(point: array, rot_point: array, rot_angle: int) -> array:
    a = radians(rot_angle)
    x, y = point - rot_point
    return array((
        x * cos(a) - y * sin(a),
        x * sin(a) + y * cos(a)
    )) + rot_point


def affinate_point(point: array, direction_x: array, direction_y: array, origin: array) -> array:
    x, y = point - origin
    xx, xy = direction_x
    yx, yy = direction_y
    x0, y0 = 0, 0
    return array((
        x0 + (xx - x0) * x + (xy - x0) * y,
        y0 + (yx - y0) * x + (yy - y0) * y
    )) + origin
