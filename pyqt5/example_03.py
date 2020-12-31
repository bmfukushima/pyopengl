"""

Code from http://www.labri.fr/perso/nrougier/python-opengl/#the-hard-way

ToDo
    * Storing VAO/Programs
    * Custom VAO object for accessing meta data
    * Custom Type Modifiers attribute to add to the Fragment/Vertex shaders
        during compilation

"""
"""
Why is initialization different for setting up VAO's.
    * appears to only draw the first object...

Attribute / VAO
    Should be combined together into one object type
"""
import logging

from OpenGL.GL import (
    glGenVertexArrays,
    glBindVertexArray,
    glUseProgram,
    glPointSize,
    glDrawArrays,
    glCreateShader,
    glShaderSource,
    glCompileShader,
    glGetShaderiv,
    glGetShaderInfoLog,
    glDeleteShader,
    glCreateProgram,
    glAttachShader,
    glLinkProgram,
    glGetProgramiv,
    glGetProgramInfoLog,
    glDeleteProgram,
    glClear,
    GL_COLOR_BUFFER_BIT,
    GL_LINK_STATUS,
    GL_POINTS,
    GL_LINE_LOOP,
    GL_COMPILE_STATUS,
    GL_VERTEX_SHADER,
    GL_FRAGMENT_SHADER,
    glGetString, GL_VENDOR, GL_RENDERER, GL_VERSION, GL_SHADING_LANGUAGE_VERSION
)

from PyQt5.QtWidgets import QApplication, QOpenGLWidget
# from PyQt5.QtGui import QOpenGLWindow, QOpenGLVertexArrayObject
from PyQt5.QtCore import Qt, QPoint

from core.attribute import Attribute
from core.uniform import Uniform

logger = logging.getLogger(__name__)


class MinimalGLWidget(QOpenGLWidget):
    """
    Args:
        draw_stride (int): How many points are in the primitive type to be drawn.
            This sets the glDrawArrays stride value.
        draw_type (GL_DRAW_TYPE):
            GL_POINTS, GL_LINE_LOOP, GL_TRIANGLE_FAN, GL_TRIANGLES
        _resizing (bool): determines if this widget is currently being resized or not
        _object_list (list): of all currently active VAO's to be drawn by the paintGL call

    Notes:
        - update() calls the paintGL function
        - resizeEvent() --> resizeGL() --> paintGL()
            resizeEvent is doing a glClear, and this is very hard to start =\
                UPDATE BEHAVIOR by default is to clear on paintGL
                use "setUpdateBehavior(PartialUpdate | NoPartialUpdate)"
                    PartialUpdate is default
        - for some reason the paintGL runs twice on init

        -
    """
    # vertex shader
    VERTEX_SHADER_DEFAULT = """
            in vec3 position;
            in vec3 vertex_color;
            uniform vec3 translation;
            out vec3 color;

            void main()
            {
                vec3 pos = position + translation;
                gl_Position = vec4(pos, 1.0);
                color = vertex_color;
            }
            """
    FRAGMENT_SHADER_DEFAULT = """
            in vec3 color;
            void main()
            {
                gl_FragColor = vec4(color, 1.0);
                //gl_FragColor = vec4(1.0, 0.5, 1.0, 1.0);
            }
            """

    def __init__(self, parent=None, draw_stride=0, draw_type=GL_POINTS):
        super(MinimalGLWidget, self).__init__(parent)
        self._global_object_list = []
        self._object_list = []
        #self._resizing = False
        self._draw_stride = draw_stride
        self._draw_type = draw_type

        # UPDATE PROGRAM
        self.resized.connect(self.test)

        # UNIFORMS

    def test(self):
        print('yolo')

    # todo move creation of primitives into this
    def createPolygon(self, points_list, colors_list=None):

        # make current
        self.makeCurrent()

        # generate VAO and set as ACTIVE
        polygon_vao = glGenVertexArrays(1)
        glBindVertexArray(polygon_vao)

        # setup POINTS
        pos_attr = Attribute("vec3", points_list)
        pos_attr.associateReference(self.program(), "position")

        # setup COLOR
        if colors_list:
            col_attr = Attribute("vec3", colors_list)
            col_attr.associateReference(self.program(), "vertex_color")

        return polygon_vao

    def initializeGL(self):
        """
        Run each time a call to update OpenGL is sent
        :return:
        """
        print ('--> initializeGL')
        # set update mode https://doc.qt.io/qt-5/qopenglwidget.html#UpdateBehavior-enum
        self.setUpdateBehavior(QOpenGLWidget.PartialUpdate)

        # program (fragment, vertex)
        program = MinimalGLWidget.initializeProgram()
        self.setProgram(program)

        MinimalGLWidget.printSystemInfo()
        # UNIFORM | keyboard translation
        self.user_translation = Uniform("vec3", [0.0, 0.0, 0.0])
        self.user_translation.locateVariable(program, "translation")

        colors = [
            [1.0, 0.5, 0.5],
            [0.5, 1.0, 0.5],
            [0.5, 0.5, 1.0]
        ]

        # CREATE PRIMITIVES
        points = [
            [0.8, 0.8, 0.0],
            [0.8, 0.2, 0.0],
            [0.2, 0.2, 0.0]
        ]
        self.triangle0 = self.createPolygon(points, colors_list=colors)

        points = [
            [-0.4, -0.4, 0.0],
            [-0.8, -0.2, 0.0],
            [-0.2, -0.2, 0.0]

        ]
        self.triangle1 = self.createPolygon(points, colors_list=colors)

        # polygon
        points = [
            [-0.5, 0.5, 0.0],
            [-0.8, 0.8, 0.0],
            [-0.2, 0.8, 0.0],
        ]

        self.poly = self.createPolygon(points, colors_list=colors)
        # why did they detach the shader?
        # will need to shaders from program?
        #glDetachShader(program, vertex)
        #glDetachShader(program, fragment)

        glPointSize(20)

        self.update([self.triangle0, self.triangle1], draw_stride=3)

    def paintGL(self):
        """
        Has to be called to send signal to draw to OpenGL?
        :return:
        """
        # preflight
        #self.setUpdateBehavior(QOpenGLWidget.PartialUpdate)

        # this is drawing them on top of each other, due to new shaders
        for vao in self._global_object_list:
            glBindVertexArray(vao)
            glDrawArrays(self.drawType(), 0, self.drawStride())

        return QOpenGLWidget.paintGL(self)

    # def resizeGL(self, width, height):
    #     print('resize GL')
    #     # self._resizing = True
    #     # self._object_list = self._global_object_list
    #     # print("object liset === ", self._object_list)
    #     return QOpenGLWidget.resizeGL(self, width, height)
    #
    # def resizeEvent(self, event):
    #     # This will block the clear event...
    #     #self.res
    #     print('resize event')
    #     return self.resizeGL(self.width(), self.height())
    #     #return
    #
    # def resized(self):
    #     print('resized')
    #     self.doneCurrent()
    #     pass
    # def aboutToResize(self):
    #     print('about to resize')
    #     self.doneCurrent()
    #     pass

    """ EVENTS """
    def keyPressEvent(self, event):
        """
        Todo: Uniforms
            why do uniforms just explode...
        """
        wasd = [Qt.Key_W, Qt.Key_A, Qt.Key_S, Qt.Key_D]
        translation_amount = 0.1
        if event.key() in wasd:
            # self.makeCurrent()
            if event.key() == Qt.Key_W:
                self.user_translation.data[1] += translation_amount
            elif event.key() == Qt.Key_A:
                self.user_translation.data[0] -= translation_amount
            elif event.key() == Qt.Key_S:
                self.user_translation.data[1] -= translation_amount
            elif event.key() == Qt.Key_D:
                self.user_translation.data[0] += translation_amount

            # upload data
            self.makeCurrent()
            self.user_translation.uploadData()
            self.doneCurrent()

            # redraw
            self.redraw(clear=True)

        if event.key() == Qt.Key_Q:
            self.user_translation.data = [0.25, 0.25, 0.0]

            self.update(self._global_object_list)

            # vertex_source = """
            #     in vec3 position;
            #     in vec3 vertex_color;
            #     out vec3 color;
            #     void main()
            #     {
            #         gl_Position = vec4(position.x * 0.5, position.y * 0.5, position.z * 0.5, 1.0);
            #         color = vertex_color;
            #     }
            # """
            # fragment_source = """
            #     in vec3 color;
            #     void main()
            #     {
            #         gl_FragColor = vec4(color, 1.0);
            #     }
            # """
            # # need make current for poly creation /shrug
            # points = [
            #     [0.5, -0.5, 0.0],
            #     [0.8, -0.8, 0.0],
            #     [0.2, -0.8, 0.0],
            # ]
            # colors = [
            #     [1.0, 0.5, 0.5],
            #     [0.5, 1.0, 0.5],
            #     [0.5, 0.5, 1.0]
            # ]
            # #self.makeCurrent()
            # self.another_one = self.createPolygon(points, colors_list=colors)
            #
            # self.update(
            #     [self.poly, self.another_one],
            #     stride=3,
            #     clear=False,
            #     primitive_type=GL_LINE_LOOP,
            #     fragment_source_code=fragment_source,
            #     vertex_source_code=vertex_source
            # )

        return QOpenGLWidget.keyPressEvent(self, event)

    def redraw(self, clear=False):
        self.update(self._global_object_list, clear=clear)

    def update(
            self,
            vao_list,
            draw_stride=None,
            draw_type=None,
            clear=False,
            vertex_source_code=None,
            fragment_source_code=None
        ):
        # START STATE UPDATE
        self.makeCurrent()

        # setup draw attrs
        if draw_type:
            self.setDrawType(draw_type)
        if draw_stride:
            self.setDrawStride(draw_stride)

        # update object lists
        for object in vao_list:
            if object not in self._global_object_list:
                self._global_object_list.append(object)
        self._object_list = vao_list

        # clear
        if clear:
            glClear(GL_COLOR_BUFFER_BIT)

        # update program if new vertex/fragment code is provided
        if vertex_source_code or fragment_source_code:
            program = self.initializeProgram(vertex_source_code=vertex_source_code, fragment_source_code=fragment_source_code)
            self.setProgram(program)
            # TODO how to set up association?
            # does association even matter??

        # bind VAO
        for vao in vao_list:
            glBindVertexArray(vao)
            glDrawArrays(self.drawType(), 0, self.drawStride())

        # update
        self.doneCurrent()

        # draw
        return QOpenGLWidget.update(self)

    """ PROPERTIES """
    def program(self):
        return self._program

    def setProgram(self, program):
        self._program = program
        glUseProgram(program)

    def drawType(self):
        return self._draw_type

    def setDrawType(self, _draw_type):
        self._draw_type = _draw_type

    def drawStride(self):
        return self._draw_stride

    def setDrawStride(self, _draw_stride):
        self._draw_stride = _draw_stride

    """ UTILS """
    @staticmethod
    def initializeShader(shaderCode, shaderType):
        extension = "#extension GL_ARB_shading_language_420pack: require \n"
        shader_code = "#version 130 \n" + extension + shaderCode

        # create the shader
        shader = glCreateShader(shaderType)

        # link shader code
        glShaderSource(shader, shader_code)

        # compile shader
        glCompileShader(shader)

        # check shader
        compile_success = glGetShaderiv(shader, GL_COMPILE_STATUS)

        # if shader fails
        if not compile_success:
            # get error message
            error_message = glGetShaderInfoLog(shader)

            # delete shader
            glDeleteShader(shader)

            # decode error message from bit to utf-8
            error_message = "\n" + error_message.decode("utf-8")

            raise Exception(error_message)

        # shader successful compilation
        return shader

    @staticmethod
    def initializeProgram(vertex_source_code=None, fragment_source_code=None):
        """
        Creates a new shader program based off of the source code provided.

        If not source is provided, a default one will be constructed from this
        classes attributes.

        Args:
            vertex_source_code (GLSL): in string format
            fragment_source_code (GLSL): in string format
        Returns:
            reference to a PROGRAM

        Pipeline:
            1.) Get source code
            2.) Create SHADER
            3.) Create PROGRAM
            4.) Attach SHADER'S to PROGRAM
            5.) Create executable to run on GPU
            6.) Error checking
        """

        ## GET SOURCE CODE
        # vertex shader
        if not vertex_source_code:
            vertex_source_code = MinimalGLWidget.VERTEX_SHADER_DEFAULT
        # fragment shader
        if not fragment_source_code:
            fragment_source_code = MinimalGLWidget.FRAGMENT_SHADER_DEFAULT

        # CREATE SHADERS
        vertex_shader = MinimalGLWidget.initializeShader(vertex_source_code, GL_VERTEX_SHADER)
        fragment_shader = MinimalGLWidget.initializeShader(fragment_source_code, GL_FRAGMENT_SHADER)

        ## CREATE PROGRAM
        program = glCreateProgram()

        ## ATTACH SHADERS TO PROGRAM
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)

        ## CREATE GPU EXECUTABLE
        glLinkProgram(program)

        ## ERROR CHECKING
        success = glGetProgramiv(program, GL_LINK_STATUS)
        if not success:
            # get error message
            message = glGetProgramInfoLog(program)

            # delete program
            glDeleteProgram(program)

            # convert error message from bit --> utf-8
            message = "\n" + message.decode("utf-8")

            # print error message
            raise Exception(message)

        ## FINISH ERROR CHECKING
        return program

    @staticmethod
    def printSystemInfo():
        print ("=====" * 10)
        #info_types = [GL.GL_VENDOR, GL.GL_RENDERER, GL.GL_VERSION, GL.GL_SHADING_LANGUAGE_VERSION]
        print("Vendor:", glGetString(GL_VENDOR).decode('utf-8'))
        print("Renderer:", glGetString(GL_RENDERER).decode('utf-8'))
        print("GL Support:", glGetString(GL_VERSION).decode('utf-8'))
        print("GLSL Support:", glGetString(GL_SHADING_LANGUAGE_VERSION).decode('utf-8'))
        print("=====" * 10)


if __name__ == '__main__':
    app = QApplication([])
    widget = MinimalGLWidget()
    widget.show()
    app.exec_()