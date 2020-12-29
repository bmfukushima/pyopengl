"""
zoom event
    GLWidget --> QMousePressEvent --> QMouseMoveEvent --> paintGL --> zoomEvent()
pan event
    GLWidget -->  QMousePressEvent --> QMouseMoveEvent --> panEvent --> paintGL
"""

import sys
import math

from PyQt5.QtCore import pyqtSignal, QPoint, QPointF, QSize, Qt
from PyQt5.QtGui import QColor, QCursor, QPainter, QFont
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QOpenGLWidget, QSlider,
                             QWidget)

import OpenGL.GL as GL
#from OpenGL.raw.GL.VERSION.GL_1_0 import GL_PROJECTION


class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()

        self.glWidget = GLWidget()
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.glWidget)
        self.setLayout(mainLayout)
        self.setWindowTitle("Hello GL")


class GLWidget(QOpenGLWidget):
    """
Args:
    **  zoomFactor (float): User defined zoom factor exposed for the API.
    ** panFactor (float): User defined pan factor exposded for the API.
Attributes:

    *   pan_pos (QPoint): The current position of the camera
    *   zoom_factor (int): The total zoom factor based off of how far the
            user has moved the cursor during a zoom event multiplied by
            the user set zoom factor ( setZoomFactor() )
    """
    def __init__(
        self,
        parent=None
    ):
        super(GLWidget, self).__init__(parent)

    def getOpenglInfo(self):
        info = """
Vendor: {0}
Renderer: {1}
OpenGL Version: {2}
Shader Version: {3}
        """.format(
            GL.glGetString(GL.GL_VENDOR),
            GL.glGetString(GL.GL_RENDERER),
            GL.glGetString(GL.GL_VERSION),
            GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION)
        )

        return info

    def drawGrid(self):
        pass
        
        GL.glPolygonMode(GL.GL_FRONT, GL.GL_LINE)
        
        GL.glLineWidth(1)
        GL.glBegin(GL.GL_LINES)
        half_num_lines = int(self.zoom_factor) + 1
        full_num_lines = int((self.zoom_factor * 2)) + 1
        print(1/full_num_lines)
        GL.glColor4f(1, 1, 1, 1/full_num_lines)
        for x in range(-half_num_lines, half_num_lines):
            # draw vertical lines
            GL.glVertex3f(x, half_num_lines, -5)
            GL.glVertex3f(x, -half_num_lines, -5)
            
            # draw horizontal lines
            
        GL.glEnd()
    """ EVENTS """
    def initializeGL(self):
        print(self.getOpenglInfo())

        GL.glClearColor(0.18, 0.18, 0.18, 1.0)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glMatrixMode(GL.GL_MODELVIEW)

    def paintGL(self):

        GL.glLoadIdentity()
        GL.glTranslatef(0, 0, -5)

        # set color
        GL.glColor4f(0, 1, 0, .5)
        # set drawing mode
        GL.glLineWidth(5)
        # enable transparency
        GL.glDisable(GL.GL_CULL_FACE)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        #glDisable(GL_CULL_FACE)
        GL.glPolygonMode(GL.GL_FRONT, GL.GL_FILL)
        point_list = [0.5, 0.25]
        GL.glBegin(GL.GL_TRIANGLES)
        for x in point_list:
            GL.glVertex3f(-x, -x, x)
            GL.glVertex3f(0, x, x)
            GL.glVertex3f(x, -x, x)

        GL.glEnd()
        #self.drawGrid()

    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        GL.glViewport((width - side) // 2, (height - side) // 2, side, side)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
        GL.glMatrixMode(GL.GL_MODELVIEW)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    pos = QCursor.pos()
    window.show()
    window.setGeometry(pos.x() - 320, pos.y() - 240, 640, 480)
    sys.exit(app.exec_())
