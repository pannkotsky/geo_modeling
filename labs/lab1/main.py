import sys

sys.path.append('..')  # noqa

import wx
from OpenGL import GL
from wx import glcanvas

from helpers import refresh2d
from lab1.kangaroo import get_kangaroo
from lab1.swan import get_swan

# canvas constants
WIDTH, HEIGHT = 604, 604
PADDING = 20
FULL_WIDTH = WIDTH + PADDING * 2
FULL_HEIGHT = HEIGHT + PADDING * 2

TOTAL_STEPS = 50
INTERVAL = 20


class OpenGLCanvas(glcanvas.GLCanvas):
    def __init__(self, parent):
        attribList = (glcanvas.WX_GL_RGBA,  # RGBA
                      glcanvas.WX_GL_DOUBLEBUFFER,  # Double Buffered
                      glcanvas.WX_GL_DEPTH_SIZE, 24)  # 24 bit
        super().__init__(parent, -1, attribList=attribList, size=(FULL_WIDTH, FULL_HEIGHT))
        self.parent = parent
        self.is_gl_initialized = False
        self.init_drawing()
        self.context = glcanvas.GLContext(self)

    def init_drawing(self):
        self.current_step = 0
        self.outline1 = get_kangaroo()
        self.outline2 = get_swan()

    def on_paint(self, event: wx.Event):
        self.SetCurrent(self.context)
        if not self.is_gl_initialized:
            self.init_gl()
        self.on_draw()
        event.Skip()

    def on_draw(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()  # reset position
        refresh2d(FULL_WIDTH, FULL_HEIGHT)  # set mode to 2d

        self.draw()

        self.SwapBuffers()

    def draw(self):
        GL.glColor3f(0.0, 0.0, 0.0)
        self.outline1.intermediate(self.outline2, TOTAL_STEPS, self.current_step).draw()

    def init_gl(self):
        GL.glClearColor(1.0, 1.0, 1.0, 1.0)


class MyPanel(wx.Panel):
    def __init__(self, parent, *args, **kw):
        super().__init__(parent, *args, **kw)
        self.canvas = OpenGLCanvas(self)
        self.forward_timer = wx.Timer(self)
        self.back_timer = wx.Timer(self)

        self.full_back_btn = wx.Button(self, -1, "<<", pos=(FULL_WIDTH + 20, 20), size=(30, 30))
        self.back_btn = wx.Button(self, -1, "<", pos=(FULL_WIDTH + 55, 20), size=(30, 30))
        self.forward_btn = wx.Button(self, -1, ">", pos=(FULL_WIDTH + 90, 20), size=(30, 30))
        self.full_forward_btn = wx.Button(self, -1, ">>", pos=(FULL_WIDTH + 125, 20), size=(30, 30))

        self.Bind(wx.EVT_BUTTON, self.on_full_back, source=self.full_back_btn)
        self.Bind(wx.EVT_BUTTON, self.on_back, source=self.back_btn)
        self.Bind(wx.EVT_BUTTON, self.on_forward, source=self.forward_btn)
        self.Bind(wx.EVT_BUTTON, self.on_full_forward, source=self.full_forward_btn)

        self.Bind(wx.EVT_TIMER, self.on_back_timer, source=self.back_timer)
        self.Bind(wx.EVT_TIMER, self.on_forward_timer, source=self.forward_timer)

        self.Bind(wx.EVT_PAINT, self.canvas.on_paint)

    def on_full_back(self, event):
        self.back_timer.StartOnce(INTERVAL)

    def on_back_timer(self, event):
        if self.canvas.current_step > 0:
            self.canvas.current_step -= 1
            self.Refresh()
            self.back_timer.StartOnce(INTERVAL)

    def on_back(self, event):
        if self.canvas.current_step > 0:
            self.canvas.current_step = max(self.canvas.current_step - 10, 0)

    def on_forward(self, event):
        if self.canvas.current_step < TOTAL_STEPS:
            self.canvas.current_step = min(self.canvas.current_step + 10, TOTAL_STEPS)

    def on_full_forward(self, event):
        self.forward_timer.StartOnce(INTERVAL)

    def on_forward_timer(self, event):
        if self.canvas.current_step < TOTAL_STEPS:
            self.canvas.current_step += 1
            self.Refresh()
            self.forward_timer.StartOnce(INTERVAL)


class MyFrame(wx.Frame):
    def __init__(self):
        self.size = (FULL_WIDTH + 200, FULL_HEIGHT + 20)
        super().__init__(None, title='Lab 1', size=self.size)
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
