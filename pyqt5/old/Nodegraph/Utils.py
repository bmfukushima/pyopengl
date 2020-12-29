import numpy
import multiprocessing

from PyQt5.QtGui import (
    QOpenGLFramebufferObjectFormat, QOpenGLFramebufferObject,
    QOpenGLPaintDevice, QPainter, QColor, QFont
)
from PyQt5.QtCore import QPointF, Qt

from OpenGL import GL


class NodegraphSprite(object):
    '''
    '''

    def __init__(self, udim):
        self.udim = udim
        self.node_list = []

    """ PROPERTIES """
    @property
    def udim(self):
        return self._udim

    @udim.setter
    def udim(self, udim):
        self._udim = udim

    @property
    def node_list(self):
        return self._node_list

    @node_list.setter
    def node_list(self, node_list):
        self._node_list = node_list

    @property
    def cached_texture(self):
        self._cached_texture

    @cached_texture.setter
    def cached_texture(self, cached_texture):
        self._cached_texture = cached_texture

    """ UTILS """
    def addNode(self, node):
        self.node_list.append(node)


class NodegraphCache(object):
    """
    Interface for the nodegraph caching mechanism.  This has been
    broken out into a seperate class, and used in multi inheritance
    for organizational reasons.

    Attributes:
        bottom_left (QPointF): The camera's starting location for the 1001
            UDIM.
        min_pos (QPointF): The min point found in the point list
    """
    cache_resolution = 2048
    chunk_size = 100

    def cacheNodegraph(self, node_list):
        """
        Saves the entire nodegraph into square textures with
        UDIM coordinates
        """
        # store default values
        orig_pan_pos = self.pan_pos
        orig_width = self.width()
        orig_height = self.height()

        # setup attrs
        #node_list = numpy.array(node_list)
        node_list = numpy.array([node[:-1] for node in node_list])
        self.setWidth(self.cache_resolution)
        self.setHeight(self.cache_resolution)
        self.nodegraph_sprites = {}

        # get bounds
        minv = numpy.amin(node_list, axis=0)
        xmin = minv[0]
        ymin = minv[1]
        maxv = numpy.amax(node_list, axis=0)
        xmax = maxv[0]
        ymax = maxv[1]
        self.min_pos = QPointF(xmin, ymin)
        width = xmax - xmin
        height = ymax - xmin
            # resolution? zoom distance?
        # get bottom left corner
        #node_width = 5
        #node_height = 5
        '''
        self.bottom_left = QPointF(
            -(xmin + self.chunk_size - node_width),
            ymin + self.chunk_size - node_height
        )
        '''
        self.bottom_left = QPointF(
            -(xmin),
            ymin
        )
        # get column / row count
        self.num_col = int(width / (self.chunk_size * 2)) + 2
        self.num_row = int(height / (self.chunk_size * 2)) + 2

        # create frame buffer object
        format = QOpenGLFramebufferObjectFormat()
        format.setAttachment(QOpenGLFramebufferObject.CombinedDepthStencil)
        m_fbo = QOpenGLFramebufferObject(self.cache_resolution, self.cache_resolution, format)
        for c in range(self.num_col):
            for r in range(self.num_row):
                # set attrs
                self.zoom_factor = self.chunk_size
                udim = '10{0}{1}'.format(r, c+1)
                self.nodegraph_sprites[udim] = NodegraphSprite(udim=udim)

                # offset camera
                camxpos = self.bottom_left.x() - c * (self.chunk_size * 2)
                camypos = self.bottom_left.y() + r * (self.chunk_size * 2)
                self.pan_pos = QPointF(camxpos, camypos)
                # update GL
                m_fbo.bind()

                # draw GL
                GL.glViewport(0, 0, self.cache_resolution, self.cache_resolution)
                self.cacheGL(udim)
                #GL.glPolygonMode(GL.GL_FRONT, GL.GL_FILL)
                self.paintUDIM(udim, camxpos, camypos)

                # write image
                image = m_fbo.toImage()
                image_file = '/media/ssd01/dev/temp/temp/10{0}{1}.png'.format(r, c+1)
                self.nodegraph_sprites[udim].cached_texture = image_file
                image.save(image_file)

        # restore default values
        self.pan_pos = orig_pan_pos
        self.setWidth(orig_width)
        self.setHeight(orig_height)

        pass

    def paintUDIM(self, udim, camxpos, camypos):
        
        painter, fbo_paint_dev = self.createTextFBO(self.cache_resolution, self.cache_resolution)
        #painter.drawText(20, 40, '{0} \n {1},{2}'.format(udim, camxpos, camypos))
        painter.drawText(20, 40, self.width(), self.height(), Qt.AlignLeft, '{0} \n {1},{2}'.format(udim, camxpos, camypos))
        painter.end()

    def createTextFBO(
            self,
            width,
            height,
            color=QColor().fromRgbF(1.0, 1.0, 1.0, 1.0),
            font='Arial',
            font_size=8
            ):
        """
        Creates a painting device for writing text to.

        Args:
            width (int): the width of the buffer to write to
            height (int): the height of the buffer to write to
            color (QColor): color of the text
            font (string): font of text.  This is from the PyQt5
                font options.
            font_size (int): size of the font

        Returns:
            QPainter
            QOpenGLPaintDevice
        """
        # create painter
        fbo_paint_dev = QOpenGLPaintDevice(width, height)
        painter = QPainter(fbo_paint_dev)

        # set GL Rendering hints
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        GL.glPolygonMode(GL.GL_BACK, GL.GL_FILL)

        # begin native painting
        painter.beginNativePainting()
        painter.endNativePainting()

        # set up painter attrs
        painter.setPen(color)
        painter.setFont(QFont(font, font_size))

        return painter, fbo_paint_dev

    """ PROPERTIES """

    @property
    def bottom_left(self):
        return self._bottom_left

    @bottom_left.setter
    def bottom_left(self, bottom_left):
        self._bottom_left = bottom_left

    @property
    def min_pos(self):
        return self._min_pos

    @min_pos.setter
    def min_pos(self, min_pos):
        self._min_pos = min_pos


def startMultithreadedProcess(list, func, **kwargs):
        """
        Breaks a list into chunks, and runs a function on
        a seperate process for each one of those chunks.

        Args:
            *   list (list): list to break into chunks
            *   func (func): function to run on the individual chunk.
                    This should take one argument, a list.
            ** data_type (str): the type of data to draw.  This will either
                    be 'shape' or 'text'
            ** udim (str): the current udim number that is being cached

        """
        if len(list) > 0:
            core_count = multiprocessing.cpu_count()
            chunk_size = int(len(list) / core_count)
            for core in range(core_count):
                if (core + 1) != core_count:
                    chunk = list[chunk_size*core:chunk_size*(core+1)]
                else:
                    chunk = list[chunk_size*core:-1]
                    chunk.append(list[0])
                    chunk.append(list[-1])
                p = multiprocessing.Process(
                    target=func(
                        chunk, kwargs
                    )
                )
                p.start()


def convertWorldToScreen(x, y, widget):
    """
    Converts world space coordinates to screen space coordinates.
    This assumes the default cartesian plane for world  of

                    +1
                      |
            -1  ------   +1
                      |
                    -1

    Args:
        x (int): x coordinate, in world space
        y (int): y coordinate, in world space
        widget (QOpenGLWindow): widget whose screen space you want
            to convert to.  The wigdet will need the following attrs
                pan_pos (QPoint)
                height (int)
                width (int)
                zoom_factor (float)
                aspect_ratio (float)
    """
    y -= widget.pan_pos.y()
    y *= -1 # flip y orientation ( see note above)
    y /= widget.zoom_factor # factor zoom
    y += 1 # offset cartesian plane
    y *= (widget.height() * 0.5)
    # offset

    # CALCULATE XPOS
    x /= widget.aspect_ratio
    x += widget.pan_pos.x() / widget.aspect_ratio
    x /= widget.zoom_factor
    x += 1
    x *= (widget.width() * 0.5)

    return x, y


def convertWorldToCamera(x, y, widget):
    """
    Converts world space coordinates to screen space coordinates.
    This assumes the default cartesian plane for world  of

                    +1
                      |
            -1  ------   +1
                      |
                    -1

    Args:
        x (int): x coordinate, in world space
        y (int): y coordinate, in world space
        widget (QOpenGLWindow): widget whose screen space you want
            to convert to.  The wigdet will need the following attrs
                pan_pos (QPoint)
                aspect_ratio (float)
    """
    pan_x = widget.pan_pos.x() / widget.aspect_ratio
    x /= widget.aspect_ratio
    x += pan_x

    y -= widget.pan_pos.y()
    return x, y


def renderScreen():
    pass


def getTime():
    """
    Returns the current time in seconds.  Used to calculate FPS.
    """
    import datetime
    ms = datetime.datetime.utcnow().microsecond * 0.0000001
    s = datetime.datetime.utcnow().second
    return ms + s
'''
temp_list = [-10, -5, 0, 5, 10]
# x pos
# y pos
# node
point_list = []

for x in temp_list:
    point = []
    point.append(x)
    point.append(x)
    point.append(0.5)
    point_list.append(point)

cacheNodegraph(point_list)
'''