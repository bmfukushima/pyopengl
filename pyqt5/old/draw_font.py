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
        parent=None,
        zoomFactor=1.0,
        panFactor=1.0
    ):
        super(GLWidget, self).__init__(parent)
        # User Attrs
        self.setZoomFactor(zoomFactor)
        self.setPanFactor(panFactor)

        # Initialize default attrs
        self._zoom_factor = 1
        self._zoom_active = False
        self._pan_active = False
        self._pan_pos = QPoint(0, 0)

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
        """
        draws the background grid
        """
        # get extra attrs
        half_num_lines = int(self.zoom_factor * self.aspect_ratio) + 2
        full_num_lines = int((self.zoom_factor * 2)) + 2
        x_offset, _ = math.modf(self.pan_pos.x())
        y_offset, _ = math.modf(self.pan_pos.y())

        # setup GL
        GL.glPolygonMode(GL.GL_FRONT, GL.GL_LINE)
        GL.glLineWidth(1)
        GL.glColor4f(1, 1, 1, 1)
        GL.glBegin(GL.GL_LINES)

        # draw lines
        for x in range(-half_num_lines, half_num_lines):
            # draw vertical lines
            GL.glVertex3f(((x + x_offset) / self.aspect_ratio), half_num_lines, 5)
            GL.glVertex3f(((x + x_offset) / self.aspect_ratio), -half_num_lines, 5)
            # draw horizontal lines
            GL.glVertex3f(half_num_lines, x - y_offset, 5)
            GL.glVertex3f(-half_num_lines, x - y_offset, 5)

        GL.glEnd()

    def drawFont(self):
        print('draw font')
        # need to set the polygon mode to fill, or else it will turn into
        # some nasty artifacting thingy
        GL.glPolygonMode(GL.GL_FRONT, GL.GL_FILL)
        painter = QPainter(self)
        painter.beginNativePainting()
        painter.endNativePainting()

        color = QColor().fromRgbF(1, 0, 0, 1)
        painter.setPen(color)
        painter.setFont(QFont("Arial", 8 / self.zoom_factor))

        xpos = 0
        ypos = 0
        pan_x = self.pan_pos.x()# * self.aspect_ratio
        x_pos = (pan_x + xpos) * self.width()
        y_pos = -(self.pan_pos.y() * (self.height())) * .5 / self.zoom_factor
        #print(x_pos, y_pos)
        painter.drawText(x_pos, y_pos, self.width(), self.height(), Qt.AlignLeft, "Hello World!")
        """
        for x in range(50):
            for y in range(50):
                #painter.drawText(x * 75, y * 10,"Hello World!");
                painter.drawText(x * 75, y * 10, self.width(), self.height(), Qt.AlignLeft, "Hello World!")
        """

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
        GL.glColor3f(0, 1, 0)
        self.drawGrid()
        self.drawFont()

        # update camera
        self.zoomEvent()

    def zoomEvent(self):
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()

        GL.glOrtho(
            (- .5 * self.zoom_factor) * 2,
            + 1 * self.zoom_factor,
            (- .5 * self.zoom_factor) * 2,
            + 1 * self.zoom_factor,
            0.0,
            15.0
        )

        try:
            # zoom at position
            zoom_offset = self.zoom_factor - self._orig_zoom_factor

            xpos = (self._start_pos.x() / self.width()) * 2 - 1
            ypos = (self._start_pos.y() / self.height()) * 2 - 1

            panx = float((self._orig_pan_pos.x() + (zoom_offset * xpos)  * self.aspect_ratio ))
            pany = float((self._orig_pan_pos.y() + (zoom_offset * ypos)))

            self.pan_pos = QPointF(panx, pany)
        except AttributeError:
            pass

    def panEvent(self, x, y):
        """
        translates the global camera as a pan event

        Args:
            x (int): How many units to move the camera in the
                x direction
            y (int): How many units to move the camera in the
                y direction
        """
        x *= self.getPanFactor() * 0.01
        y *= self.getPanFactor() * 0.01
        x += self._orig_pan_pos.x()
        y += self._orig_pan_pos.y()
        self.pan_pos = QPointF(x, y)

    def resizeGL(self, width, height):
        GL.glViewport(0, 0, self.width(), self.height())
        self.zoomEvent()

    def mousePressEvent(self, event, *args, **kwargs):
        modifiers = QApplication.keyboardModifiers()

        # zoom
        if ( 
            (modifiers == Qt.AltModifier) and
            (event.button() == Qt.RightButton)
        ):
            self._zoom_active = True
            self._start_pos = event.pos()
            self._orig_zoom_factor = self.zoom_factor

        # pan
        if (event.button() == Qt.MiddleButton):
            self._pan_active = True
            self._start_pos = event.pos()
            self._orig_pan_pos = self.pan_pos
        return QOpenGLWidget.mousePressEvent(self, event, *args, **kwargs)

    def mouseMoveEvent(self, event, *args, **kwargs):
        # zoom
        if self._zoom_active is True:
            # get magnitude
            orig_pos = self._start_pos
            cur_pos = event.pos()
            zoom_offset = math.sqrt(
                math.pow(cur_pos.x() - orig_pos.x(), 2) +
                math.pow(cur_pos.y() - orig_pos.y(), 2)
            )
            # check cursor direction
            if cur_pos.x() - orig_pos.x() > 0:
                zoom_offset *= -1
            zoom_offset *= 0.1 * self.getZoomFactor()
            # get zoom factor
            self.zoom_factor = self._orig_zoom_factor + zoom_offset
            if self.zoom_factor < .5:
                self.zoom_factor = .5

        # pan
        if self._pan_active is True:
            orig_pos = self._start_pos
            cur_pos = event.pos()
            x = cur_pos.x() - orig_pos.x()
            y = cur_pos.y() - orig_pos.y()
            self.panEvent(x, y)
            # redraw GL

        self.update()

        return QOpenGLWidget.mouseMoveEvent(self, event, *args, **kwargs)

    def mouseReleaseEvent(self, *args, **kwargs):
        self._zoom_active = False
        self._pan_active = False
        return QOpenGLWidget.mouseReleaseEvent(self, *args, **kwargs)

    """ API """
    def getZoomFactor(self):
        return self._user_zoom_factor

    def setZoomFactor(self, user_zoom_factor):
        self._user_zoom_factor = user_zoom_factor

    def getPanFactor(self):
        return self._user_pan_factor

    def setPanFactor(self, user_pan_factor):
        self._user_pan_factor = user_pan_factor

    """ PROPERTIES """
    @property
    def aspect_ratio(self):
        return self.width() / self.height()

    @property
    def pan_pos(self):
        return self._pan_pos

    @pan_pos.setter
    def pan_pos(self, pan_pos):
        self._pan_pos = pan_pos

    @property
    def zoom_factor(self):
        return self._zoom_factor

    @zoom_factor.setter
    def zoom_factor(self, zoom_factor):
        self._zoom_factor = zoom_factor


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    pos = QCursor.pos()
    window.show()
    window.setGeometry(pos.x() - 320, pos.y() - 240, 640, 480)
    sys.exit(app.exec_())
