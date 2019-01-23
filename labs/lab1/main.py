import sys

sys.path.append('..')  # noqa

import wx
from OpenGL import GL
from wx import glcanvas

from helpers import refresh2d
from lab1.kangaroo import get_kangaroo

# canvas constants
WIDTH, HEIGHT = 413, 604
PADDING = 20
FULL_WIDTH = WIDTH + PADDING * 2
FULL_HEIGHT = HEIGHT + PADDING * 2


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
        self.outline1 = get_kangaroo()
        self.current_outline = self.outline1

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

        self.current_outline.draw()

    def init_gl(self):
        GL.glClearColor(1.0, 1.0, 1.0, 1.0)


class MyPanel(wx.Panel):
    def __init__(self, parent, *args, **kw):
        super().__init__(parent, *args, **kw)
        self.canvas = OpenGLCanvas(self)

        self.Bind(wx.EVT_PAINT, self.canvas.on_paint)


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
