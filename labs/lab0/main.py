import sys

sys.path.append('..')  # noqa

import numpy
import wx
from OpenGL import GL, GLUT
from wx import glcanvas

from helpers import refresh2d
from lab0.utils import draw_grid, draw_point, get_object

# canvas constants
WIDTH, HEIGHT = 900, 600
PADDING = 40
ORIGIN = numpy.array((WIDTH // 2, HEIGHT // 2))

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
        self.object = get_object(ORIGIN)
        self.rot_point = ORIGIN + (0, 0)

        self.context = glcanvas.GLContext(self)

        self.Bind(wx.EVT_LEFT_UP, self.on_mouse_click)

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

        draw_grid(ORIGIN, WIDTH - PADDING * 2, HEIGHT - PADDING * 2, 20)
        draw_point(self.rot_point)
        self.object.draw()

        self.SwapBuffers()

    def on_mouse_click(self, event: wx.MouseEvent):
        self.rot_point = numpy.array((event.x, HEIGHT - event.y))
        self.parent.rot_x_input.SetValue(event.x - ORIGIN[0])
        self.parent.rot_y_input.SetValue(HEIGHT - event.y - ORIGIN[1])

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

        self.reset_btn = wx.Button(self, -1, "Reset", pos=(WIDTH + 20, 280), size=(100, 30))

        self.Bind(wx.EVT_BUTTON, self.on_shift, source=self.shift_apply_btn)
        self.Bind(wx.EVT_BUTTON, self.on_rotate, source=self.rot_apply_btn)
        self.Bind(wx.EVT_BUTTON, self.on_reset, source=self.reset_btn)
        self.Bind(wx.EVT_PAINT, self.canvas.on_paint)
        self.Bind(wx.EVT_KEY_UP, self.on_key_press)
        self.canvas.Bind(wx.EVT_KEY_UP, self.on_key_press)

    def on_shift(self, event):
        self.canvas.object.shift(self.shift_x_input.GetValue(), self.shift_y_input.GetValue())

    def on_rotate(self, event):
        rot_point = ORIGIN + (
            self.rot_x_input.GetValue(),
            self.rot_y_input.GetValue()
        )
        rot_angle = self.rot_angle_input.GetValue()
        self.canvas.object.rotate(rot_point, rot_angle)
        self.canvas.rot_point = rot_point

    def on_reset(self, event):
        self.canvas.object = get_object(ORIGIN)
        self.canvas.rot_point = ORIGIN + (0, 0)
        self.shift_x_input.SetValue(0)
        self.shift_y_input.SetValue(0)
        self.rot_x_input.SetValue(0)
        self.rot_y_input.SetValue(0)
        self.rot_angle_input.SetValue(0)

    def on_key_press(self, event: wx.KeyEvent):
        key_code = event.KeyCode
        ctrl_down = event.ControlDown()
        if key_code == wx.WXK_LEFT:
            if ctrl_down:
                self.canvas.object.rotate(self.canvas.rot_point, ROTATE_STEP)
            else:
                self.canvas.object.shift(-SHIFT_STEP, 0)
            self.Refresh()
        elif key_code == wx.WXK_RIGHT:
            if ctrl_down:
                self.canvas.object.rotate(self.canvas.rot_point, -ROTATE_STEP)
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
        self.size = (WIDTH + 140, HEIGHT + 50)
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
