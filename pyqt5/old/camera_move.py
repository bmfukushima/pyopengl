import sys
import math

from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QOpenGLWidget, QSlider,
                             QWidget)

import OpenGL.GL as gl
from OpenGL.raw.GL.VERSION.GL_1_0 import GL_PROJECTION


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
        self.zoom_factor = 1
        self.zoom_active = False

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
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glRotate(0,1,1,45)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        #self.object = self.makeObject()
        #gl.glShadeModel(gl.GL_FLAT)
        #gl.glEnable(gl.GL_DEPTH_TEST)
        #gl.glEnable(gl.GL_CULL_FACE)

    def paintGL(self):
        # camera points towards -z axis
        # viewport has coordinates of 1 unit
        #gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
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

        # update camera
        self.zoomEvent()

    def zoomEvent(self):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(
            -1 * self.zoom_factor,
            +1 * self.zoom_factor,
            +1 * self.zoom_factor,
            -1 * self.zoom_factor,
            0.0,
            15.0
        )
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def resizeGL(self, width, height):
        self.zoomEvent()

    def mousePressEvent(self, event, *args, **kwargs):
        modifiers = QApplication.keyboardModifiers()
        if ( 
            (modifiers == Qt.AltModifier) and
            (event.button() == Qt.RightButton)
        ):
            self.zoom_active = True
            self.zoom_start_pos = event.pos()
            self._orig_zoom_factor = self.zoom_factor

        return QOpenGLWidget.mousePressEvent(self, event, *args, **kwargs)

    def mouseMoveEvent(self, event, *args, **kwargs):
        # zoom
        if self.zoom_active is True:
            # get magnitude
            orig_pos = self.zoom_start_pos
            cur_pos = event.pos()
            print(orig_pos, cur_pos)
            zoom_offset = math.sqrt(
                math.pow(cur_pos.x() - orig_pos.x(), 2) +
                math.pow(cur_pos.y() - orig_pos.y(), 2)
            )
            # check cursor direction
            if cur_pos.x() - orig_pos.x() > 0:
                zoom_offset *= -1
            zoom_offset *= .001
            # get zoom factor
            self.zoom_factor = self._orig_zoom_factor + zoom_offset
            if self.zoom_factor < .5:
                self.zoom_factor = .5

            # redraw GL
            self.update()

        return QOpenGLWidget.mouseMoveEvent(self, event, *args, **kwargs)

    def mouseReleaseEvent(self, *args, **kwargs):
        self.zoom_active = False
        return QOpenGLWidget.mouseReleaseEvent(self, *args, **kwargs)

    """ PROPERTIES """
    """
    zoom_active (boolean): Returns True if in a zoom operation,
        else returns false.
    zoom_factor (int): How much the current zoom is
    zoom_start_pos (QPoint): The starting position of the cursor
        when a zoom operation begins
    """
    @property
    def zoom_active(self):
        return self._zoom_active

    @zoom_active.setter
    def zoom_active(self, zoom_active):
        self._zoom_active = zoom_active

    @property
    def zoom_factor(self):
        return self._zoom_factor

    @zoom_factor.setter
    def zoom_factor(self, zoom_factor):
        self._zoom_factor = zoom_factor

    @property
    def zoom_start_pos(self):
        return self._zoom_start_pos

    @zoom_start_pos.setter
    def zoom_start_pos(self, zoom_start_pos):
        self._zoom_start_pos = zoom_start_pos


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    pos = QCursor.pos()
    window.show()
    window.setGeometry(pos.x() - 320, pos.y() - 240, 640, 480)
    #window.move(pos)
    sys.exit(app.exec_())
