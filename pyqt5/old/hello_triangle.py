import sys
import math

from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QOpenGLWidget, QSlider,
                             QWidget)

import OpenGL.GL as gl


class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()

        self.glWidget = GLWidget()
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.glWidget)
        self.setLayout(mainLayout)
        self.setWindowTitle("Hello GL")


class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.zoom_factor = 2
    def getOpenglInfo(self):
        info = """
Vendor: {0}
Renderer: {1}
OpenGL Version: {2}
Shader Version: {3}
        """.format(
            gl.glGetString(gl.GL_VENDOR),
            gl.glGetString(gl.GL_RENDERER),
            gl.glGetString(gl.GL_VERSION),
            gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION)
        )

        return info

    def initializeGL(self):
        print(self.getOpenglInfo())
        #viewport = gl.glViewport(0, 0, 500, 500)
        gl.glClearColor(0.18, 0.18, 0.18, 1.0)
        #self.object = self.makeObject()
        #gl.glShadeModel(gl.GL_FLAT)
        #gl.glEnable(gl.GL_DEPTH_TEST)
        #gl.glEnable(gl.GL_CULL_FACE)

    def paintGL(self):
        # camera points towards -z axis
        # viewport has coordinates of 1 unit
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        gl.glTranslatef(0, 0, -5)

        # set color
        gl.glColor3f(0, 1, 0)
        # set drawing mode
        gl.glLineWidth(5)
        gl.glPolygonMode(gl.GL_FRONT, gl.GL_LINE)
        gl.glBegin(gl.GL_TRIANGLES)
        gl.glVertex3f(-0.5, -0.5, .5)
        gl.glVertex3f(0, 0.5, .5)
        gl.glVertex3f(0.5, -0.5, .5)

        gl.glVertex3f(-0.25, -0.25, .25)
        gl.glVertex3f(0, 0.25, .25)
        gl.glVertex3f(0.25, -0.25, .25)

        gl.glEnd()

    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        gl.glViewport((width - side) // 2, (height - side) // 2, side, side)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    pos = QCursor.pos()
    window.show()
    window.setGeometry(pos.x() - 320, pos.y() - 240, 640, 480)
    #window.move(pos)
    sys.exit(app.exec_())
