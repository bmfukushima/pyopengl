"""
zoom event
    GLWidget --> QMousePressEvent --> QMouseMoveEvent --> paintGL --> zoomEvent()
pan event
    GLWidget -->  QMousePressEvent --> QMouseMoveEvent --> panEvent --> paintGL

To Do

Ideas
    ReDraw Strategies..
        Implemented:
            *  prune:
                    remove every nth element if the fps drops below a certain
                    threshold ( 35 fps)
            *  freeze updates:
                    does not update if the fps drops below
                    a certain threshold ( 5 fps ).

        Not Implemented
            - proxy display
                change display from fill/line/solid to primitive, remove excess as
                the node gets smaller on screen.
            - area
                remove if area smaller than x
            - multiple layers...
                draw to multiple buffers, only update the buffers that are active
                    - PyQt5 QLayerStack
                        Might be slow?  Have to calculate a lot of qRects...
                    - Different frame buffers?
                    - Save layers to images and load images with hitboxes...

"""

import sys
import math
import random
import datetime
import multiprocessing

from PyQt5.QtCore import QPoint, QPointF, Qt
from PyQt5.QtGui import QColor, QCursor, QPainter, QFont, QOpenGLWindow, QRegion
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QWidget, QVBoxLayout, QStackedLayout)

import OpenGL.GL as GL


class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()

        self.glWidget = GLWidget()
        proxy_container = self.createWindowContainer(self.glWidget, self)
        proxy_container.setLayout(QVBoxLayout())
        proxy_resize = QWidget()
        proxy_container.layout().addWidget(proxy_resize)

        self.triangle = TestLayer()
        region = QRegion(self.triangle.frameGeometry())
        self.triangle.setMask(region)
        proxy_container1 = self.createWindowContainer(self.triangle, self)
        proxy_container1.setLayout(QVBoxLayout())
        proxy_resize1 = QWidget()
        proxy_container1.layout().addWidget(proxy_resize1)

        main_layout = QStackedLayout()
        main_layout.setStackingMode(QStackedLayout.StackAll)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(proxy_container)
        main_layout.addWidget(proxy_container1)

        self.setLayout(main_layout)

    def resizeEvent(self, *args, **kwargs):
        return QWidget.resizeEvent(self, *args, **kwargs)


class GLWidget(QOpenGLWindow):
    """
Nodegraph base class.

This holds all of the necessary parts to draw the Nodegraph.  Additional
GL drawing layers can be added, however the base layer is the grid...

Args:
    **  gridOpacity (bool): Determines whether or not the grid lines will be
            dimmed based off of their distance to the camera.
    **  panFactor (float): User defined pan factor exposded for the API.
    **  zoomFactor (float): User defined zoom factor exposed for the API.

Attributes:
    *   aspect_ratio (float): The aspect ratio of the current window
    *   fps (float): The number of frames drawn per second...
    *   pan_pos (QPoint): The current position of the camera
    *   redraw (boolean): If open GL will update.  If the FPS drops below
            the minimum threshold ( 5 fps ) this will become enabled during
            the camera move.
    *   zoom_factor (int): The total zoom factor based off of how far the
            user has moved the cursor during a zoom event multiplied by
            the user set zoom factor ( setZoomFactor() )
    """
    def __init__(
        self,
        parent=None,
        zoomFactor=1.0,
        panFactor=1.0,
        gridOpacity=True
    ):
        super(GLWidget, self).__init__(parent)
        # User Attrs
        self.setGridOpactiy(gridOpacity)
        self.setZoomFactor(zoomFactor)
        self.setPanFactor(panFactor)

        # Initialize default attrs
        self._zoom_factor = 10.0
        self._orig_zoom_factor = self._zoom_factor
        self._zoom_active = False
        self._pan_active = False
        self._pan_pos = QPoint(1, 1)
        self._orig_pan_pos = self._pan_pos
        self._start_pos = QPoint(1, 1)
        self._redraw = True
        self._fps = 35
        self._prune_rate = 1
        self._prune_index = 0

    def initializeGL(self):
        GL.glClearColor(0.18, 0.18, 0.18, 1.0)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glMatrixMode(GL.GL_MODELVIEW)

        # create dummy points list
        self.point_list = []
        num_points = 10
        for x in range(num_points):
            point = {}
            point['size'] = 0.5
            point['xpos'] = random.randrange(0, 10)
            point['ypos'] = random.randrange(0, 10)
            self.point_list.append(point)
        #self.point_generator = (point for point in self.point_list)

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

    """ UTILS """
    def getFPS(self):
        """
        Gets the current FPS

        Returns:
            (str)
        """
        start_time = self._start_time
        end_time = datetime.datetime.utcnow().microsecond
        microseconds = end_time - start_time
        if microseconds < 1:
            microseconds = 1
        fps = 1000000 / microseconds
        fps = "{:.2f}".format(round(fps, 2))
        return fps

    def drawFPS(self, fps):
        """
        Displays the FPS in the upper right corner of the display

        Args:
            *   fps (float|int|str): the current FPS
        """
        GL.glPolygonMode(GL.GL_FRONT, GL.GL_FILL)
        painter = QPainter(self)
        painter.beginNativePainting()
        painter.endNativePainting()

        color = QColor().fromRgbF(1.0, 1.0, 1.0, 1.0)
        painter.setPen(color)
        painter.setFont(QFont("Arial", 16))
        painter.drawText(0, 0, self.width(), self.height(), Qt.AlignRight, str(fps))

    def drawGrid(self):
        """
        draws the background grid
        """
        # get extra attrs
        half_num_lines = int(self.zoom_factor * self.aspect_ratio) + 2
        full_num_lines = int((self.zoom_factor * 2)) + 2
        x_offset, _ = math.modf(self.pan_pos.x())
        y_offset, _ = math.modf(self.pan_pos.y())
        if self.getGridOpactiy() is True:
            opacity = (1/full_num_lines) * 12
        else:
            opacity = 1

        # setup GL
        GL.glPolygonMode(GL.GL_FRONT, GL.GL_LINE)
        GL.glLineWidth(1)
        GL.glColor4f(1, 1, 1, opacity)
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

    def drawNodes(self):
        def draw(points_list):
            """
            Heavy lifting of drawing, this will check to see if the position is in camera,
            and if it is, draw it in the scene
            """
            for index, point in (enumerate(points_list)):
                if index % self._prune_rate == self._prune_index % self._prune_rate:
                    size = point['size']
                    xpos = point['xpos'] / self.aspect_ratio
                    ypos = point['ypos']
                    bound = (self.zoom_factor + 1) + 1
                    pan_x = self.pan_pos.x() / self.aspect_ratio
                    if (
                        (-bound < (xpos + pan_x < bound)) and
                        (-bound < (ypos - self.pan_pos.y()) < bound)
                    ):
                        # if zoom over a certain distance... do something?
                        GL.glVertex3f((-size / self.aspect_ratio) + pan_x + xpos, -size - self.pan_pos.y() + ypos, 3)
                        GL.glVertex3f(0 + pan_x + xpos, size - self.pan_pos.y() + ypos, 3)
                        GL.glVertex3f((size / self.aspect_ratio) + pan_x + xpos, -size - self.pan_pos.y() + ypos, 3)

        self._prune_index += 1
        # set drawing modes
        GL.glLineWidth(5)
        GL.glPolygonMode(GL.GL_FRONT, GL.GL_LINE)
        GL.glColor4f(0, 1, 0, 0.5)

        # enable transparency
        #GL.glEnable(GL.GL_CULL_FACE)
        GL.glDisable(GL.GL_MULTISAMPLE)

        # DRAW TRIANGLES
        GL.glBegin(GL.GL_TRIANGLES)

        # prune method
        if self._pan_active is True or self._zoom_active is True:
            while float(self.fps) < 15:
                self._prune_rate += 2
                self.fps = self.getFPS()
                self.update()
        else:
            self._prune_rate = 1

        # this needs to be multi threaded
        core_count = multiprocessing.cpu_count()
        chunk_size = int(len(self.point_list) / core_count)
        for core in range(core_count):
            if (core + 1) != core_count:
                chunk = self.point_list[chunk_size*core:chunk_size*(core+1)]
            else:
                chunk = self.point_list[chunk_size*core:-1]
            p = multiprocessing.Process(target=draw(chunk))
            p.start()

        GL.glEnd()

    """ EVENTS """
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

        GL.glMatrixMode(GL.GL_MODELVIEW)

    def panEvent(self, x, y):
        """
        translates the global camera as a pan event

        Args:
            x (int): How many units to move the camera in the
                x direction
            y (int): How many units to move the camera in the
                y direction
        """
        x *= self.getPanFactor() * 0.0025 * self.zoom_factor
        y *= self.getPanFactor() * 0.0025 * self.zoom_factor
        x += self._orig_pan_pos.x()
        y += self._orig_pan_pos.y()
        #print(self.pan_pos)
        self.pan_pos = QPointF(x, y)

    def paintGL(self):
        # start fps timer
        self._start_time = datetime.datetime.utcnow().microsecond
        ### SET UP GL
        # clear buffer
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        # load matrix
        GL.glLoadIdentity()
        GL.glTranslatef(0, 0, -5)

        ### DRAW
        # grid
        self.drawGrid()

        # node
        self.drawNodes()

        # fps
        self.fps = self.getFPS()

        self.drawFPS(self.fps)
        fps = int(float(self.fps))
        if fps < 5:
            self.redraw = False

        # update camera
        self.zoomEvent()

    def resizeGL(self, width, height):
        # causes initial snap on pan...
        # GL.glViewport(0, 0, self.width(), self.height())
        self.zoomEvent()

    def mousePressEvent(self, event, *args, **kwargs):
        modifiers = QApplication.keyboardModifiers()
        self._prune_index = 0
        # zoom
        if (
            (modifiers == Qt.AltModifier) and
            (event.button() == Qt.RightButton)
        ):
            self._zoom_active = True
            self._start_pos = event.pos()
            self._orig_zoom_factor = self.zoom_factor
            self._orig_pan_pos = self.pan_pos

        # pan
        if (event.button() == Qt.MiddleButton):
            self._pan_active = True
            self._start_pos = event.pos()
            self._orig_pan_pos = self.pan_pos
        return QOpenGLWindow.mousePressEvent(self, event, *args, **kwargs)

    def mouseMoveEvent(self, event, *args, **kwargs):
        # zoom
        if self._zoom_active is True:
            """
            This needs to run here or as we need to define the
            zoom_factor before the update() is called
            """
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
            self.zoom_factor = zoom_offset + self._orig_zoom_factor
            """
            # GET ZOOM FACTOR
            # set zoom speed relative to the current zoom factor
            relative_threshhold = 50

            if zoom_offset != 0:
                current_zoom = (self._orig_zoom_factor + zoom_offset)
                if (current_zoom < relative_threshhold):# and (zoom_offset < 0):
                    #zoom_offset = current_zoom / zoom_offset
                    #print(zoom_offset)
                    zoom_offset = zoom_offset / relative_threshhold
                    self.zoom_factor += zoom_offset
                else:
                    self.zoom_factor = current_zoom

            if zoom_offset != 0:
                current_zoom = (self._orig_zoom_factor + zoom_offset)
                if (current_zoom < relative_threshhold):# and (zoom_offset < 0):
                    zoom_offset = current_zoom / zoom_offset
                    print(zoom_offset)
                    #zoom_offset = zoom_offset / relative_threshhold
            self.zoom_factor = self._orig_zoom_factor + zoom_offset
            """

            # minimum bound
            if self.zoom_factor < 5.0:
                self.zoom_factor = 5.0

        # pan
        if self._pan_active is True:
            orig_pos = self._start_pos
            cur_pos = event.pos()
            x = cur_pos.x() - orig_pos.x()
            y = cur_pos.y() - orig_pos.y()
            self.panEvent(x, y)
            # redraw GL

        self.update()

        return QOpenGLWindow.mouseMoveEvent(self, event, *args, **kwargs)

    def mouseReleaseEvent(self, *args, **kwargs):
        # reset attrs
        self._zoom_active = False
        self._pan_active = False
        self._redraw = True
        self._prune_rate = 1

        self.update()

        # delete excess attrs
        try:
            delattr(self, '_orig_zoom_factor')
        except AttributeError:
            pass

        return QOpenGLWindow.mouseReleaseEvent(self, *args, **kwargs)

    """ API """
    def getGridOpactiy(self):
        return self._grid_opacity

    def setGridOpactiy(self, grid_opacity):
        self._grid_opacity = grid_opacity

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
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, fps):
        self._fps = fps

    @property
    def redraw(self):
        return self._redraw

    @redraw.setter
    def redraw(self, redraw):
        self._redraw = redraw

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


class TestLayer(QOpenGLWindow):
    def __init__(self, parent=None):
        super(TestLayer, self).__init__(parent)
        self.zoom_factor = 2
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
        #viewport = GL.glViewport(0, 0, 500, 500)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glClearColor(0.18, 0.18, 0.18, 0.0)
        #self.object = self.makeObject()
        #GL.glShadeModel(GL.GL_FLAT)
        #GL.glEnable(GL.GL_DEPTH_TEST)
        #GL.glEnable(GL.GL_CULL_FACE)

    def paintGL(self):
        # camera points towards -z axis
        # viewport has coordinates of 1 unit
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()
        GL.glTranslatef(0, 0, -5)

        # set color
        GL.glColor3f(0, 1, 0)
        # set drawing mode
        GL.glLineWidth(5)
        GL.glPolygonMode(GL.GL_FRONT, GL.GL_LINE)
        GL.glBegin(GL.GL_TRIANGLES)
        GL.glVertex3f(-0.5, -0.5, .5)
        GL.glVertex3f(0, 0.5, .5)
        GL.glVertex3f(0.5, -0.5, .5)

        GL.glVertex3f(-0.25, -0.25, .25)
        GL.glVertex3f(0, 0.25, .25)
        GL.glVertex3f(0.25, -0.25, .25)

        GL.glEnd()

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
