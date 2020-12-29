"""
TEST
#===============================================================================
# TO DO
#===============================================================================
* make object/shaders...
    Where should this init?
        - initGL
            need to be smarter about updates and how updates work..
        - paintGL
            slow af...
                because it destroys the cpu
Optimization:
    * When running through the points list to check if it is in the UDIM sector...
        it runs through the point list multiple times... instead of only running through it
        once... and storing this cache into the UDIMs...
            currently...
                for udim, check all points
            better...
                for point in points:
                    put in udim area...

    * Nodegraph Caching
        - Only create what's needed during cache, instead of creating everything...
            Utils.cacheNodegraph()

    * Are sprites flawed?
        - can possible instance sprites for every individual item...

* transparency on zoom...
    nodes are dissappearing wayyyy to fast...
#===============================================================================
# BUGS
#===============================================================================
* fps calculation from date time is wrong...
    - only grabbing micro seconds...
    - if second rolls over during.. will provide the wrong result

#===============================================================================
# EVENTS
#===============================================================================
zoom event
    Nodegraph --> mousePressEvent --> mouseMoveEvent --> paintGL --> zoomEvent()
    Nodegraph --> wheelEvent --> paintGL --> zoomEvent()
pan event
    Nodegraph -->  QMousePressEvent --> QMouseMoveEvent --> panEvent --> paintGL
cache event
    cache
        Nodegraph
            | -- initializeGL
                | -- Utils.cacheNodegraph
                    | -- cacheGL
                        | -- drawAllNodes
                            | -- drawNodeShape
    reproject
        object creation:
            initializeGL
                | -- createShader
                | -- makeObject
        painting
            Nodegraph --> paintGL --> drawAllNodegraphSprites()


Layers:
    Grid
    Node Draw ( textured planes )
    Selection
    Node Link...
    Node Move
    HUD
        Paint Text Overlays (HUD)
        HUD Widgets

To Do

Ideas
    Node Optimization:
        Middle out
            - Compile a model of the Nodegraph Positions
            - Search from postion clicked by user in the model.
            - Stop searching when node is out of bounds
            - Needs to update the list when a node is moved...
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

import math
import numpy
import sys

from PyQt5.QtCore import QPointF, Qt, QRect
from PyQt5.QtGui import (
    QColor, QCursor, QPainter, QFont, QOpenGLWindow,
    QOpenGLFramebufferObjectFormat, QOpenGLFramebufferObject,
    QOpenGLPaintDevice, QOpenGLShader, QOpenGLShaderProgram,
    QMatrix4x4, QOpenGLTexture, QImage
)
from PyQt5.QtWidgets import (
    QApplication, QHBoxLayout, QWidget, QVBoxLayout
)

from OpenGL import GL

from Utils import (
    NodegraphCache, convertWorldToScreen,
    convertWorldToCamera, startMultithreadedProcess,
    getTime
)

from HUDLayer import TextLayer
from Node import Node, Parameter, Port
from GridLayer import GridLayer


class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()
        self.glWidget = NodegraphDelegate()

        proxy_container = self.createWindowContainer(self.glWidget, self)
        proxy_container.setLayout(QVBoxLayout())
        proxy_resize = QWidget()
        proxy_container.layout().addWidget(proxy_resize)

        mainLayout = QHBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(proxy_container)
        self.setLayout(mainLayout)

    def resizeEvent(self, *args, **kwargs):
        return QWidget.resizeEvent(self, *args, **kwargs)


class NodegraphSpriteUtils(object):
    """ OPEN GL """

    def makeObject(self):
        """
        Creates all of the image planes for the texture reprojection
        process.  This will also create all necessary data to go with it
        such as texture coords, uv's, and the texture list to be displayed
        """
        self.texCoords = []
        self.vertices = []
        self.texture_list = []
        coords = []

        file_path = '/media/ssd01/dev/temp/temp'
        for r in range(self.num_row):
            for c in range(self.num_col):
                # set attrs
                GL.glViewport(0, 0, self.cache_resolution, self.cache_resolution)
                udim = '10{0}{1}'.format(r, c+1)
                # check to see if udim exists...
                if len(self.nodegraph_sprites[udim].node_list) > 0:
                    '''
                    why tf is this drawing some sprites that just don't exist...
                    '''
                    # could also do a texture check... so..
                    self.texture_list.append(
                        QOpenGLTexture(QImage('%s/%s.png' %(file_path, udim)))
                    )

                    # offset camera
                    camxpos = self.bottom_left.x() + c * (self.chunk_size * 2)
                    camypos = self.bottom_left.y() - r * (self.chunk_size * 2)
                    left = camxpos - self.chunk_size
                    right = camxpos + self.chunk_size
                    top = camypos + self.chunk_size
                    bottom = camypos - self.chunk_size
                    coords = (
                        (left, bottom, self.SPRITE_DEPTH),
                        (right, bottom, self.SPRITE_DEPTH),
                        (right, top, self.SPRITE_DEPTH),
                        (left, top, self.SPRITE_DEPTH)
                    )

                    self.texCoords += [(0, 0), (1, 0), (1, 1),  (0, 1)]
                    for i in range(4):
                        x, y, z = coords[i]
                        self.vertices.append((x, y, z))

    def createShader(self):
        self.PROGRAM_VERTEX_ATTRIBUTE, self.PROGRAM_TEXCOORD_ATTRIBUTE = range(2)

        # CREATE SHADERS
        self.createVertexShader()
        self.createFragmentShader()
        # vertex
        vshader = QOpenGLShader(QOpenGLShader.Vertex, self)
        vshader.compileSourceCode(self.vsrc)
        # fragment
        fshader = QOpenGLShader(QOpenGLShader.Fragment, self)
        fshader.compileSourceCode(self.fsrc)

        # COMPILE SHADERS
        self.program = QOpenGLShaderProgram()
        self.program.addShader(vshader)
        self.program.addShader(fshader)
        self.program.bindAttributeLocation(
            'vertex', self.PROGRAM_VERTEX_ATTRIBUTE
        )
        self.program.bindAttributeLocation(
            'texCoord', self.PROGRAM_TEXCOORD_ATTRIBUTE
        )

    def bindShader(self):
        self.program.link()

        self.program.bind()
        self.program.setUniformValue('texture', 0)

        self.program.enableAttributeArray(self.PROGRAM_VERTEX_ATTRIBUTE)
        self.program.enableAttributeArray(self.PROGRAM_TEXCOORD_ATTRIBUTE)
        self.program.setAttributeArray(
            self.PROGRAM_VERTEX_ATTRIBUTE, self.vertices
        )

        self.program.setAttributeArray(
            self.PROGRAM_TEXCOORD_ATTRIBUTE, self.texCoords
        )

    def createVertexShader(self):
        self.vsrc = """
attribute highp vec4 vertex;
attribute mediump vec4 texCoord;
varying mediump vec4 texc;
uniform mediump mat4 matrix;
void main(void)
{
    gl_Position = matrix * vertex;
    texc = texCoord;
}
    """

    def createFragmentShader(self):
        self.fsrc = """
uniform sampler2D texture;
varying mediump vec4 texc;
void main(void)
{
    gl_FragColor = texture2D(texture, texc.st);
}
"""


class NodegraphDelegate(
        QOpenGLWindow,
        NodegraphSpriteUtils,
        NodegraphCache,
        TextLayer,
        GridLayer
    ):
    """
Nodegraph base class.

This holds all of the necessary parts to draw the Nodegraph.  Additional
GL drawing layers can be added, however the base layer is the grid...

Grid Depth 100
Sprite Depth 90

Args:
    **  bg_color (rgbaf) clear color for the OpenGL stack
    **  fontSize (int): the default size of the system font.  This will by default
            be set proportional to the zoom factor.

            The final font size is determined by
                (fontSize * initZoomDistance) / zoom_factor
    **  initZoomDistance (float): The starting zoom distance for the camera,
            by default this is set to 10.

            Please note that the font size will remain relative to this initial
            value.  So that the only time the font size is the actual display
            value that is given, is when the current zoom distance is
            set to this value.
    **  panFactor (float): User defined pan factor exposded for the API.
    **  zoomFactor (float): User defined zoom factor exposed for the API.

Attributes:
    *   aspect_ratio (float): The aspect ratio of the current window
    *   fps (float): The number of frames drawn per second...
    *   pan_pos (QPoint): The current position of the camera
    *   zoom_factor (float): The total zoom factor based off of how far the
            user has moved the cursor during a zoom event multiplied by
            the user set zoom factor ( setZoomFactor() )
    """

    MIN_ZOOM = 20.0
    GRID_DEPTH = 100
    SPRITE_DEPTH = 90

    def __init__(
        self,
        parent=None,
        bg_color=(0.18, 0.18, 0.18, 0),
        fontSize=8,
        panFactor=1.0,
        zoomFactor=1.0,
        initZoomDistance=100.0
    ):
        # initialize multiple inheritance of all layers
        super(NodegraphDelegate, self).__init__(parent)
        GridLayer.__init__(self)

        # User Attrs
        self.setZoomFactor(zoomFactor)
        self.setPanFactor(panFactor)
        self.setFontSize(fontSize)
        self.setBGColor(bg_color)

        # Initialize default attrs
        self._init_zoom_factor = initZoomDistance
        self._zoom_factor = initZoomDistance
        self._zoom_active = False
        self._pan_active = False
        self._pan_pos = QPointF(1, 1)

    def initializeGL(self):
        # Set up Open GL
        GL.glClearColor(*self.getBGColor())
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glMatrixMode(GL.GL_MODELVIEW)

        # Enable Alpha
        GL.glEnable(GL.GL_ALPHA_TEST)
        GL.glAlphaFunc(GL.GL_GREATER, 0.01)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        # cache node graph
        self.initializeNodes()
        self.zoomEvent()
        self.cacheNodegraph(self.point_list)

        # create OpenGL Shaders
        self.makeObject()
        self.createShader()

    def initializeNodes(self):

        temp_list = [
            (-250, -250),
            (50, 50),
            (0, 0),
            (100, 100),
            (450, 450),
            (-250, -350)
        ]
        # temp_list = [-150, 0, 5, 10, 20, 25, 30, 350]
        # temp_list = [-35, -15, -10, -5]
        # x pos
        # y pos
        # node
        self.point_list = []

        for point in temp_list:

            node = Node()
            node.pos = QPointF(point[0], point[1])
            # add params
            parameters = []
            for i in range(5):
                p = Parameter()
                p.parent = None
                p.name = str('parameter_{}'.format(i))
                p.type = 'str'
            # add input ports...
            for x in range(3):
                input_port = Port()
                input_port.node = node
                input_port.name = 'in'
                input_port.type = 0
                node.input_ports.append(input_port)
            # add output ports...
            output_port = Port()
            output_port.node = node
            output_port.name = 'output'
            output_port.type = 1
            node.output_ports.append(output_port)

            new_point = []
            new_point.append(point[0])
            new_point.append(point[1])
            new_point.append(node)
            self.point_list.append(new_point)

    """ UTILS """
    def getFPS(self):
        """
        Gets the current FPS

        Returns:
            (str)
        """
        start_time = self._start_time
        end_time = getTime()
        seconds = end_time - start_time

        fps = 1 / seconds
        fps = "{:.2f}".format(round(fps, 2))
        return fps

    """ DRAWING """
    def paintGL(self):
        """
        Nodes are stored in world position.
        Camera space = World Position - Camera Position
        """

        # start fps timer
        self._start_time = getTime()

        # SET UP GL
        # clear buffer
        self.zoomEvent()

        GL.glClearColor(*self.getBGColor())
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        # load matrix
        GL.glLoadIdentity()
        GL.glTranslatef(0, 0, -10)

        # DRAW
        # grid
        self.drawGrid()

        # draw cached textures
        self.drawAllNodegraphSprites()

        # fps - this needs cleanup... me no likey
        # self.fps = self.getFPS()
        # self.drawFPS()

        # draw text overlay
        self.drawTextLayer()

    def cacheGL(self, udim):
        """
        Nodes are stored in world position.
        Camera space = World Position - Camera Position
        """

        GL.glViewport(0, 0, self.cache_resolution, self.cache_resolution)
        self.zoomEvent()
        ### SET UP GL
        # clear buffer
        # clear color alpha will be used... to display...
        GL.glClearColor(*self.getBGColor())
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        # load matrix
        GL.glLoadIdentity()
        GL.glTranslatef(0, 0, -5)

        # node
        self.node_color = (1, 0, 1, 1)
        self.drawAllNodes(udim)

        self.zoomEvent()

    def drawFPS(self):
        """
        Displays the FPS in the upper right corner of the display
        """
        fps = self.getFPS()
        GL.glPolygonMode(GL.GL_BACK, GL.GL_FILL)
        painter = QPainter(self)
        painter.beginNativePainting()
        painter.endNativePainting()

        color = QColor().fromRgbF(1.0, 1.0, 1.0, 1.0)
        painter.setPen(color)
        painter.setFont(QFont("Arial", 16))
        # Qt::TextWordWrap
        rect = QRect(0, 0, self.width(), self.height())
        painter.drawText(
            rect,
            Qt.AlignRight,
            #"""%sasdf %s \n test""" % (fps, self.zoom_factor)
            '%s test'%self.zoom_factor
        )
        painter.end()

    def drawAllNodes(self, udim, test=False):
        """
        In charge of drawing all of the nodes.  The nodes
        must be converted from world space to camera space
        in order to be visible in render.

        Notes:
                    +1
                      |
            -1  ------   +1
                      |
                    -1
        """
        def draw(points_list, kwargs):
            """
            Heavy lifting of drawing, this will check to see if the position is in camera,
            and if it is, draw it in the scene

            Args:
                points_list (list): list of points, eventually this will probably be changed
                    to the actual nodes list.
                draw_type (str): options of 'node' or 'text' to determine if this should draw
                    the actual node shape, or the text for the node.
            """

            draw_type = kwargs['draw_type']
            udim = kwargs['udim']
            test = kwargs['test']
            if len(points_list) > 0:
                # pre flight check to determine if node should be rendered.
                l = numpy.array(points_list)
                bound = (self.zoom_factor + 1) + 1
                pan_x = self.pan_pos.x() / self.aspect_ratio
                points_list = l[
                        ((l[:, 0] / self.aspect_ratio + pan_x) <= bound)
                    & ((l[:, 0] / self.aspect_ratio + pan_x) >= -bound)
                    & ((l[:, 1] - self.pan_pos.y()) <= bound)
                    & ((l[:, 1] - self.pan_pos.y()) >= -bound)
                ]

                # Draw nodes
                for point in points_list:
                    if test is False:
                        self.nodegraph_sprites[udim].addNode(point)
                    node = point[2]
                    if draw_type == 'shape':
                        self.drawNodeShape(node)
                    elif draw_type == 'text':
                        self.drawNodeText(node)

        GL.glDisable(GL.GL_MULTISAMPLE)

        # DRAW TRIANGLES
        # multi threaded (Python
        startMultithreadedProcess(self.point_list, draw, draw_type='shape', udim=udim, test=test)
        startMultithreadedProcess(self.point_list, draw, draw_type='text', udim=udim, test=test)

    def drawNodeText(self, node):
        """
        Draws font at the specified x, y coordinates.  The coordinates provided
        are world coordinates from the OpenGL scene.

        This will automagically convert the world coordinates from the GL scene
        to screen space.

        Args:
            x (float): global x coord in the OpenGL scene
            y (float): global y coord in the OpenGL scene
        Note:
            x/y pos is relative to the zoom factor, so if the zoom factor is 10
            then the total cartesian plane is -10 , +10.

            That in the painter/widget (0,0) and (1,1) is in the bottom right
            While the GL viewport is set to (0,0) at the center, and (1,1) in the top right,
            thus flipping the Y Axis
            Need to map this to widget coordinates for height/width...

            GL.glPolygonMode:
            need to set the polygon mode to fill, or else it will turn into
            some nasty artifacting thingy
        """

        # get attrs
        font_size = self.getFontSize() * self._init_zoom_factor
        font_size = int(font_size / self.zoom_factor)
        x = node.pos.x()
        y = node.pos.y()

        # temp attrs
        orig_x = x
        orig_y = y

        # pre flight checks
        if font_size < 2: return

        # set up painter
        color = QColor().fromRgbF(0, 1, 0, 1)
        painter, fbo_paint_dev = self.createTextFBO(
            self.width(), self.height(), color=color, font_size=font_size
        )

        x, y = convertWorldToScreen(x, y, self)
        # unneccesary text offset, just so it doesnt sit in the middle of the node...
        #x += 15
        # draw
        painter.drawText(x, y, self.width(), self.height(), Qt.AlignLeft, "(%s, %s)"%(orig_x, orig_y))
        painter.end()

    def drawNodeShape(self, node):
        """
        Draws the node shape of an individual node.

        Args:
            x (float): global x coord in the OpenGL scene
            y (float): global y coord in the OpenGL scene
            size (float): size of the node (height/width)
                This will change in the future to actually support
                nodes... instead of just primitive shapes lulz.
        """

        # set GL node drawing
        color = self.node_color
        GL.glColor4f(color[0], color[1], color[2], color[3])
        GL.glPolygonMode(GL.GL_BACK, GL.GL_FILL)
        GL.glLineWidth(2)
        GL.glBegin(GL.GL_QUADS)

        # convert world to camera
        x = node.pos.x()
        y = node.pos.y()
        # size = .5
        x, y = convertWorldToCamera(x, y, self)

        # draw vertexs

        width = node.width / self.aspect_ratio
        height = node.height

        # draw from upper left
        GL.glVertex3f(x, y, node.depth)
        GL.glVertex3f(width + x, y, node.depth)
        GL.glVertex3f(width + x, y - height, node.depth)
        GL.glVertex3f(x, y - height, node.depth)

        self.drawNodePortShapes(x, y, node)
        '''
        # Draw at center
        GL.glVertex3f(-width + x, height + y, 3)
        GL.glVertex3f(width + x, height + y, 3)
        GL.glVertex3f(width + x, -height + y, 3)
        GL.glVertex3f(-width + x, -height + y, 3)
        '''

        GL.glEnd()

    def drawNodePortShapes(self, x, y, node):
        """
        Draws all of the port shapes that are available to this node.

        If the height of all of the nodes is greater than the current
        node height, then this will adjust the node height accordingly...

        Args:
            x (float): x position in camera space
            y (float): y position in camera space
            node (Node): Node to draw the ports on
        """
        def drawPort(x, y):
            GL.glVertex3f(x, y, node.depth)
            GL.glVertex3f(x + port_size, y, node.depth)
            GL.glVertex3f(x + port_size, y - port_size, node.depth)
            GL.glVertex3f(x, y - port_size, node.depth)

        GL.glColor4f(
            self.node_color[0],
            self.node_color[1],
            self.node_color[2],
            self.node_color[3]
        )
        # get left
        # get right
        # port offset amount...
        # num ports...
        port_size = Port.size

        # input
        input_top_left_x = x - Port.spacing - port_size
        input_top_left_y = y
        for input in node.input_ports:
            drawPort(input_top_left_x, input_top_left_y)
            input_top_left_y -= port_size
            input_top_left_y -= Port.spacing

        # output
        output_top_left_x = x + Node.width + Port.spacing
        output_top_left_y = y
        for output in node.output_ports:
            drawPort(output_top_left_x, output_top_left_y)
            output_top_left_y -= port_size
            output_top_left_y -= Port.spacing

    def drawAllNodegraphSprites(self):
        #=======================================================================
        # start new GL draw...
        #=======================================================================
        self.bindShader()
        GL.glViewport(0, 0, self.width(), self.height())
        m = QMatrix4x4()
        m.ortho(-1, 1, 1, -1, 4.0, 15.0)
        '''
        xoffset = (self._min_pos.x() * 2 + 10) / self.aspect_ratio
        yoffset = - (self._min_pos.y() * 2 + 10)
        '''
        xoffset = (self._min_pos.x() * 2) / self.aspect_ratio
        yoffset = - (self._min_pos.y() * 2)
        xpos = (self.pan_pos.x() / self.aspect_ratio)
        ypos = self.pan_pos.y()

        m.translate(
            (xpos + xoffset) / self.zoom_factor,
            (ypos + yoffset) / self.zoom_factor,
            -10
        )
        m.scale(1/self.aspect_ratio, 1)
        m.scale((1/self.zoom_factor))

        self.program.setUniformValue('matrix', m)

        # draw texture array
        for i, texture in enumerate(self.texture_list):
            texture.bind()
            GL.glDrawArrays(GL.GL_TRIANGLE_FAN, i*4, 4)

        # release program
        self.vbo.unbind()
        #GL.glDisableClientState(GL.GL_VERTEX_ARRAY)
        self.program.release()

    """ EVENTS """
    def zoomEvent(self):
        """
        The zoom event will zoom the camera in/out depending on
        the user combination.  This is called at the end of every paint
        event.
        """

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()

        GL.glOrtho(
            - 1 * self.zoom_factor,
            + 1 * self.zoom_factor,
            - 1 * self.zoom_factor,
            + 1 * self.zoom_factor,
            -90,
            100
        )
        # zoom at position
        if self._zoom_active is True:
            zoom_offset = self.zoom_factor - self._orig_zoom_factor
            xpos = (self._start_pos.x() / self.width()) * 2 - 1
            ypos = (self._start_pos.y() / self.height()) * 2 - 1
            panx = float((self._orig_pan_pos.x() + (zoom_offset * xpos) * self.aspect_ratio ))
            pany = float((self._orig_pan_pos.y() + (zoom_offset * ypos)))
            self.pan_pos = QPointF(panx, pany)
        GL.glMatrixMode(GL.GL_MODELVIEW)

    def panEvent(self, x, y):
        """
        translates the global camera as a pan event

        Args:
            x (int): How many units to move the camera in the
                x direction
            y (int): How many units to move the camera in the
                y direction

        Notes:
                    +1
                      |
            +1  ------   -1
                      |
                    -1

        """

        # convert screen to camera
        x /= self.width()
        x *= (self.zoom_factor * 2 * self.aspect_ratio)
        y /= self.height()
        y *= (self.zoom_factor * 2)

        # add original position
        x += self._orig_pan_pos.x()
        y += self._orig_pan_pos.y()

        self.pan_pos = QPointF(x, y)

    def resizeGL(self, width, height):
        # causes initial snap on pan...
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

            # zoom at position attrs
            self._orig_zoom_factor = self.zoom_factor
            self._orig_pan_pos = self.pan_pos

        # pan
        if (event.button() == Qt.MiddleButton):
            self._pan_active = True
            self._start_pos = event.globalPos()
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
        # pan
        if self._pan_active is True:
            orig_pos = self._start_pos
            cur_pos = event.globalPos()
            x = cur_pos.x() - orig_pos.x()
            y = cur_pos.y() - orig_pos.y()
            self.panEvent(x, y)
            # redraw GL

        self.update()

        return QOpenGLWindow.mouseMoveEvent(self, event, *args, **kwargs)

    def mouseReleaseEvent(self, *args, **kwargs):
        # disable pan/zoom
        self._zoom_active = False
        self._pan_active = False

        return QOpenGLWindow.mouseReleaseEvent(self, *args, **kwargs)

    def wheelEvent(self, event, *args, **kwargs):
        """
        Scroll wheel zooming
        """
        self._zoom_active = True
        self._start_pos = event.pos()

        # zoom at cursor attrs
        self._orig_pan_pos = self.pan_pos
        self._orig_zoom_factor = self.zoom_factor
        # calculate the zoomies
        rotations = event.angleDelta() / 12
        self.zoom_factor -= rotations.y()

        self.zoomEvent()
        #self.update()

        # disable pan/zoom
        self._zoom_active = False
        self._pan_active = False

        return QOpenGLWindow.wheelEvent(self, event, *args, **kwargs)

    def keyPressEvent(self, event, *args, **kwargs):
        modifier = QApplication.keyboardModifiers()
        if modifier == Qt.AltModifier:
            if event.key() == Qt.Key_A:
                self.cacheNodegraph(self.point_list)
        return QOpenGLWindow.keyPressEvent(self, event, *args, **kwargs)

    """ API """
    def getBGColor(self):
        return self._bg_color[0], self._bg_color[1], self._bg_color[2], self._bg_color[3]

    def setBGColor(self, bg_color):
        self._bg_color = bg_color

    def getFontSize(self):
        return self._font_size

    def setFontSize(self, font_size):
        self._font_size = font_size

    def getPanFactor(self):
        return self._user_pan_factor

    def setPanFactor(self, user_pan_factor):
        self._user_pan_factor = user_pan_factor

    def getZoomFactor(self):
        return self._user_zoom_factor

    def setZoomFactor(self, user_zoom_factor):
        self._user_zoom_factor = user_zoom_factor

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
    def nodegraph_sprites(self):
        return self._nodegraph_sprites

    @nodegraph_sprites.setter
    def nodegraph_sprites(self, nodegraph_sprites):
        self._nodegraph_sprites = nodegraph_sprites

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
        if zoom_factor < self.MIN_ZOOM: zoom_factor = self.MIN_ZOOM
        self._zoom_factor = zoom_factor


if __name__ == '__main__':

    app = QApplication(sys.argv)
    #window = Window()
    window = NodegraphDelegate()
    pos = QCursor.pos()
    window.show()
    window.setGeometry(pos.x() - 256, pos.y() - 240, 512, 512)
    sys.exit(app.exec_())
