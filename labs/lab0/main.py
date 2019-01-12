import sys

sys.path.append('..')  # noqa

import numpy
import wx
from OpenGL import GL
from wx import glcanvas

from helpers import refresh2d
from lab0.grid import Grid
from lab0.point import Point
from lab0.utils import draw_point, get_object

# canvas constants
WIDTH, HEIGHT = 900, 680
PADDING = 40
ORIGIN = numpy.array((PADDING, PADDING))

SHIFT_STEP = 10
ROTATE_STEP = 10


class OpenGLCanvas(glcanvas.GLCanvas):
    def __init__(self, parent):
        attribList = (glcanvas.WX_GL_RGBA,  # RGBA
                      glcanvas.WX_GL_DOUBLEBUFFER,  # Double Buffered
                      glcanvas.WX_GL_DEPTH_SIZE, 24)  # 24 bit
        super().__init__(parent, -1, attribList=attribList, size=(WIDTH, HEIGHT))

        self.parent = parent

        self.is_gl_initialized = False
        self.init_drawing()

        self.context = glcanvas.GLContext(self)

    def init_drawing(self):
        self.grid = Grid(ORIGIN, WIDTH - PADDING * 2, HEIGHT - PADDING * 2, 20)
        self.object = get_object(ORIGIN + (WIDTH // 4, HEIGHT // 4))
        self.rot_point = Point(ORIGIN + (WIDTH // 4, HEIGHT // 4))

    def on_paint(self, event: wx.Event):
        self.SetCurrent(self.context)
        if not self.is_gl_initialized:
            self.init_gl()
        self.on_draw()
        event.Skip()

    def on_draw(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()  # reset position
        refresh2d(WIDTH, HEIGHT)  # set mode to 2d

        self.grid.draw()
        self.rot_point.draw()
        self.object.draw()

        self.SwapBuffers()

    def init_gl(self):
        GL.glClearColor(1.0, 1.0, 1.0, 1.0)


class MyPanel(wx.Panel):
    def __init__(self, parent, *args, **kw):
        super().__init__(parent, *args, **kw)
        self.canvas = OpenGLCanvas(self)

        wx.StaticText(self, -1, label="Shift", pos=(WIDTH + 20, 10))
        wx.StaticText(self, -1, label="x", pos=(WIDTH + 20, 32))
        self.shift_x_input = wx.SpinCtrl(self, -1, pos=(WIDTH + 60, 30), size=(60, 20), min=-WIDTH, max=WIDTH)
        wx.StaticText(self, -1, label="y", pos=(WIDTH + 20, 57))
        self.shift_y_input = wx.SpinCtrl(self, -1, pos=(WIDTH + 60, 55), size=(60, 20), min=-HEIGHT, max=HEIGHT)
        self.shift_apply_btn = wx.Button(self, -1, "Apply", pos=(WIDTH + 20, 85), size=(100, 30))

        wx.StaticText(self, -1, label="Rotation", pos=(WIDTH + 20, 135))
        wx.StaticText(self, -1, label="Pt x", pos=(WIDTH + 20, 157))
        self.rot_x_input = wx.SpinCtrl(self, -1, pos=(WIDTH + 60, 155), size=(60, 20), min=-WIDTH, max=WIDTH)
        wx.StaticText(self, -1, label="Pt y", pos=(WIDTH + 20, 182))
        self.rot_y_input = wx.SpinCtrl(self, -1, pos=(WIDTH + 60, 180), size=(60, 20), min=-HEIGHT, max=HEIGHT)
        wx.StaticText(self, -1, label="Angle", pos=(WIDTH + 20, 207))
        self.rot_angle_input = wx.SpinCtrl(self, -1, pos=(WIDTH + 60, 205), size=(60, 20), min=-360, max=360)
        self.rot_apply_btn = wx.Button(self, -1, "Apply", pos=(WIDTH + 20, 235), size=(100, 30))

        wx.StaticText(self, -1, label="Affine transform. vectors", pos=(WIDTH + 20, 285))
        wx.StaticText(self, -1, label="rx", pos=(WIDTH + 20, 307))
        self.affine_rxx_input = wx.SpinCtrlDouble(self, -1, pos=(WIDTH + 60, 305), size=(60, 20),
                                                  min=-1.5, max=1.5, initial=1, inc=0.1)
        self.affine_rxy_input = wx.SpinCtrlDouble(self, -1, pos=(WIDTH + 130, 305), size=(60, 20),
                                                  min=-1.5, max=1.5, inc=0.1)
        wx.StaticText(self, -1, label="ry", pos=(WIDTH + 20, 332))
        self.affine_ryx_input = wx.SpinCtrlDouble(self, -1, pos=(WIDTH + 60, 330), size=(60, 20),
                                                  min=-1.5, max=1.5, inc=0.1)
        self.affine_ryy_input = wx.SpinCtrlDouble(self, -1, pos=(WIDTH + 130, 330), size=(60, 20),
                                                  min=-1.5, max=1.5, initial=1, inc=0.1)
        self.affine_apply_btn = wx.Button(self, -1, "Apply", pos=(WIDTH + 20, 360), size=(100, 30))

        wx.StaticText(self, -1, label="Projective transform. axes ends", pos=(WIDTH + 20, 410))
        wx.StaticText(self, -1, label="rx", pos=(WIDTH + 20, 432))
        self.proj_rxx_input = wx.SpinCtrl(self, -1, pos=(WIDTH + 60, 430), size=(60, 20),
                                          max=WIDTH, initial=WIDTH)
        self.proj_rxy_input = wx.SpinCtrl(self, -1, pos=(WIDTH + 130, 430), size=(60, 20),
                                          max=HEIGHT)
        wx.StaticText(self, -1, label="wx", pos=(WIDTH + 20, 457))
        self.proj_wx_input = wx.SpinCtrl(self, -1, pos=(WIDTH + 60, 455), size=(60, 20),
                                         initial=1)
        wx.StaticText(self, -1, label="ry", pos=(WIDTH + 20, 482))
        self.proj_ryx_input = wx.SpinCtrl(self, -1, pos=(WIDTH + 60, 480), size=(60, 20),
                                          max=WIDTH)
        self.proj_ryy_input = wx.SpinCtrl(self, -1, pos=(WIDTH + 130, 480), size=(60, 20),
                                          max=HEIGHT, initial=HEIGHT)
        wx.StaticText(self, -1, label="wy", pos=(WIDTH + 20, 507))
        self.proj_wy_input = wx.SpinCtrl(self, -1, pos=(WIDTH + 60, 505), size=(60, 20),
                                         initial=1)
        wx.StaticText(self, -1, label="w0", pos=(WIDTH + 20, 532))
        self.proj_w0_input = wx.SpinCtrl(self, -1, pos=(WIDTH + 60, 530), size=(60, 20),
                                         max=1000, initial=WIDTH // 2)
        self.proj_apply_btn = wx.Button(self, -1, "Apply", pos=(WIDTH + 20, 560), size=(100, 30))

        self.reset_btn = wx.Button(self, -1, "Reset", pos=(WIDTH + 20, 610), size=(100, 30))

        self.Bind(wx.EVT_BUTTON, self.on_shift, source=self.shift_apply_btn)
        self.Bind(wx.EVT_BUTTON, self.on_rotate, source=self.rot_apply_btn)
        self.Bind(wx.EVT_BUTTON, self.on_reset, source=self.reset_btn)
        self.Bind(wx.EVT_BUTTON, self.on_affinate, source=self.affine_apply_btn)
        self.Bind(wx.EVT_BUTTON, self.on_project, source=self.proj_apply_btn)

        self.Bind(wx.EVT_KEY_UP, self.on_key_press)
        self.canvas.Bind(wx.EVT_KEY_UP, self.on_key_press)

        self.Bind(wx.EVT_PAINT, self.canvas.on_paint)

    def on_shift(self, event):
        self.canvas.object.shift(self.shift_x_input.GetValue(), self.shift_y_input.GetValue())

    def on_rotate(self, event):
        rot_point = ORIGIN + (
            self.rot_x_input.GetValue(),
            self.rot_y_input.GetValue()
        )
        rot_angle = self.rot_angle_input.GetValue()
        self.canvas.object.rotate(rot_point, rot_angle)
        self.canvas.rot_point = Point(rot_point)

    def on_affinate(self, event):
        direction_x = numpy.array((
            self.affine_rxx_input.GetValue(),
            self.affine_rxy_input.GetValue()
        ))
        direction_y = numpy.array((
            self.affine_ryx_input.GetValue(),
            self.affine_ryy_input.GetValue()
        ))

        for item in (self.canvas.grid, self.canvas.object, self.canvas.rot_point):
            item.affinate(direction_x, direction_y, ORIGIN)

    def on_project(self, event):
        x_end = numpy.array((
            self.proj_rxx_input.GetValue(),
            self.proj_rxy_input.GetValue()
        ))
        x_weight = self.proj_wx_input.GetValue()
        y_end = numpy.array((
            self.proj_ryx_input.GetValue(),
            self.proj_ryy_input.GetValue()
        ))
        y_weight = self.proj_wy_input.GetValue()
        origin_weight = self.proj_w0_input.GetValue()

        for item in (self.canvas.grid, self.canvas.object, self.canvas.rot_point):
            item.project(x_end, x_weight, y_end, y_weight, origin_weight, ORIGIN)

    def on_reset(self, event):
        self.canvas.init_drawing()
        self.shift_x_input.SetValue(0)
        self.shift_y_input.SetValue(0)
        self.rot_x_input.SetValue(0)
        self.rot_y_input.SetValue(0)
        self.rot_angle_input.SetValue(0)
        self.affine_rxx_input.SetValue(1)
        self.affine_rxy_input.SetValue(0)
        self.affine_ryx_input.SetValue(0)
        self.affine_ryy_input.SetValue(1)

    def on_key_press(self, event: wx.KeyEvent):
        key_code = event.KeyCode
        ctrl_down = event.ControlDown()
        if key_code == wx.WXK_LEFT:
            if ctrl_down:
                self.canvas.object.rotate(self.canvas.rot_point.point, ROTATE_STEP)
            else:
                self.canvas.object.shift(-SHIFT_STEP, 0)
            self.Refresh()
        elif key_code == wx.WXK_RIGHT:
            if ctrl_down:
                self.canvas.object.rotate(self.canvas.rot_point.point, -ROTATE_STEP)
            else:
                self.canvas.object.shift(SHIFT_STEP, 0)
            self.Refresh()
        elif key_code == wx.WXK_UP:
            self.canvas.object.shift(0, SHIFT_STEP)
            self.Refresh()
        elif key_code == wx.WXK_DOWN:
            self.canvas.object.shift(0, -SHIFT_STEP)
            self.Refresh()


class MyFrame(wx.Frame):
    def __init__(self):
        self.size = (WIDTH + 250, HEIGHT)
        super().__init__(None, title='pannkotsky', size=self.size)
        self.SetMinSize(self.size)
        self.panel = MyPanel(self)


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame()
        self.SetTopWindow(frame)
        frame.Show()
        return True


if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
    app.Destroy()
