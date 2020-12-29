import sys
import math

from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt
from PyQt5.QtGui import QColor, QCursor, QOpenGLWindow
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QOpenGLWidget, QSlider,
                             QWidget)

import OpenGL.GL as GL


class GLWidget(QOpenGLWindow):
    def __init__(self, parent=None):
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

    def initializeGL(self):
        print(self.getOpenglInfo())
        GL.glClearColor(0.18, 0.18, 0.18, 1.0)
        GL.glShadeModel(GL.GL_FLAT)
        GL.glEnable(GL.GL_DEPTH_TEST)
        #GL.glEnable(GL.GL_CULL_FACE)
        GL.glEnable(GL._CULL)

    def paintGL(self):
        GL.glLoadIdentity()
        GL.glTranslatef(0, 0, -5)
        GL.glPolygonMode(GL.GL_FRONT, GL.GL_LINE)
        GL.glLineWidth(1)
        GL.glColor4f(1, 1, 1, 1)
        GL.glLineWidth(5)
        GL.glPolygonMode(GL.GL_FRONT, GL.GL_FILL)
        #GL.glBegin(GL.GL_LINES)
        GL.glBegin(GL.GL_TRIANGLES)
        GL.glVertex3f(-0.5, -0.5, .5)
        GL.glVertex3f(0, 0.5, .5)
        GL.glVertex3f(0.5, -0.5, .5)

        GL.glVertex3f(0.25, -0.25, .25)
        GL.glVertex3f(0, 0.25, .25)

        GL.glVertex3f(-0.25, -0.25, .25)

        GL.glEnd()
        print("weiner")

    def resizeGL(self, width, height):
        #side = min(width, height)
        #if side < 0:
            #return

        #GL.glViewport((width - side) // 2, (height - side) // 2, side, side)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        #GL.glOrtho(-1, +1, -1, +1, 0.0, 15.0)
        GL.glOrtho(-1, +1, -1, +1, -10, 15.0)
        GL.glTranslatef(0, 0, -5)
        GL.glMatrixMode(GL.GL_MODELVIEW)



if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = GLWidget()
    pos = QCursor.pos()
    window.show()
    window.setGeometry(pos.x() - 320, pos.y() - 240, 640, 480)
    #window.move(pos)
    sys.exit(app.exec_())
