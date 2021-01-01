"""
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
import numpy

from OpenGL.GL import (
    glGenVertexArrays,
    glBindVertexArray,
    glUseProgram,
    glPointSize,
    glDrawArrays,
    glCreateShader, glShaderSource, glCompileShader, glGetShaderiv, glGetShaderInfoLog, glDeleteShader, glAttachShader,
    glCreateProgram, glLinkProgram, glGetProgramiv, glGetProgramInfoLog, glDeleteProgram,
    glClear,
    GL_COLOR_BUFFER_BIT,
    GL_LINK_STATUS,
    GL_POINTS,
    GL_LINE_LOOP,
    GL_COMPILE_STATUS,
    GL_VERTEX_SHADER,
    GL_FRAGMENT_SHADER,
    glGetString, GL_VENDOR, GL_RENDERER, GL_VERSION, GL_SHADING_LANGUAGE_VERSION,
    glViewport, glLoadIdentity, glOrtho, glMatrixMode, GL_PROJECTION, GL_MODELVIEW
)

from PyQt5.QtWidgets import QApplication, QOpenGLWidget
# from PyQt5.QtGui import QOpenGLWindow, QOpenGLVertexArrayObject
from PyQt5.QtCore import Qt, QPoint

from core.objectArray import ObjectArray
from core.uniform import Uniform

logger = logging.getLogger(__name__)


class OpenGLWidget(QOpenGLWidget):
    """
    Args:
        draw_stride (int): How many points are in the primitive type to be drawn.
            This sets the glDrawArrays stride value.
        draw_type (GL_DRAW_TYPE):
            GL_POINTS, GL_LINE_LOOP, GL_TRIANGLE_FAN, GL_TRIANGLES
        global_object_list (list): of all ObjectArray's that have been created
        uniforms (dict): of all of the Uniform Variables that have been created
            {name: uniform}
            Note: Uniforms can be created with createUniform

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
        super(OpenGLWidget, self).__init__(parent)
        self.global_object_list = []
        self.object_list = []
        self.uniforms = {}
        self._draw_stride = draw_stride
        self._draw_type = draw_type

    """ CREATORS """
    def createPolygon(self, points_list, colors_list=None):
        """
        Creates a new polygon from the data provided

        Args:
            colors_list (list): of lists (vec3)
            points_list (list): of lists (vec3)
        """
        # make current
        self.makeCurrent()

        # generate VAO and set as ACTIVE
        data = {"position": {"data":points_list, "data_type": "vec3"}}
        if colors_list:
            data["vertex_color"] = {"data":colors_list, "data_type": "vec3"}
        poly = ObjectArray(init_data=data, program=self.program())
        self.global_object_list.append(poly)
        return poly

    def createUniform(self, data_type, name, program, default_data):
        # UNIFORM | keyboard translation
        uniform = Uniform(data_type, default_data)
        uniform.locateVariable(program, name)
        self.uniforms[name] = uniform
        return uniform

    """ EVENTS ( DISPLAY )"""
    def initializeGL(self):
        """
        Run each time a call to update OpenGL is sent
        :return:
        """
        # set update mode https://doc.qt.io/qt-5/qopenglwidget.html#UpdateBehavior-enum
        self.setUpdateBehavior(QOpenGLWidget.PartialUpdate)

        # program (fragment, vertex)
        program = OpenGLWidget.initializeProgram()
        self.setProgram(program)

        # display system info
        OpenGLWidget.printSystemInfo()
        # UNIFORM | keyboard translation
        self.createUniform("vec3", "translation", self.program(), [0.0, 0.0, 0.0])

        # colors = [
        #     [1.0, 0.5, 0.5],
        #     [0.5, 1.0, 0.5],
        #     [0.5, 0.5, 1.0]
        # ]
        #
        # # CREATE PRIMITIVES
        # points = [
        #     [0.8, 0.8, 0.0],
        #     [0.8, 0.2, 0.0],
        #     [0.2, 0.2, 0.0]
        # ]
        # self.triangle0 = self.createPolygon(points, colors_list=colors)
        #
        # points = [
        #     [-0.4, -0.4, 0.0],
        #     [-0.8, -0.2, 0.0],
        #     [-0.2, -0.2, 0.0]
        #
        # ]
        # self.triangle1 = self.createPolygon(points, colors_list=colors)
        #
        # # polygon
        # points = [
        #     [-0.5, 0.5, 0.0],
        #     [-0.8, 0.8, 0.0],
        #     [-0.2, 0.8, 0.0],
        # ]
        #
        # self.poly = self.createPolygon(points, colors_list=colors)
        # # why did they detach the shader?
        # # will need to shaders from program?
        # #glDetachShader(program, vertex)
        # #glDetachShader(program, fragment)
        #
        # glPointSize(20)
        #
        # self.update([self.triangle0, self.triangle1], draw_stride=3)

    def paintGL(self):
        """
        Has to be called to send signal to draw to OpenGL?
        :return:
        """
        # preflight
        #self.setUpdateBehavior(QOpenGLWidget.PartialUpdate)

        # this is drawing them on top of each other, due to new shaders
        for vao in self.global_object_list:
            glBindVertexArray(vao.vao)
            glDrawArrays(self.drawType(), 0, self.drawStride())

        return QOpenGLWidget.paintGL(self)

    def update(
            self,
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

        # clear
        if clear:
            glClear(GL_COLOR_BUFFER_BIT)

        # update program if new vertex/fragment code is provided
        if vertex_source_code or fragment_source_code:
            program = self.initializeProgram(vertex_source_code=vertex_source_code, fragment_source_code=fragment_source_code)
            self.setProgram(program)
            # TODO how to set up association?
            # does association even matter??

        # update
        self.doneCurrent()

        # draw
        return QOpenGLWidget.update(self)

    def redraw(self, clear=False):
        self.update(clear=clear)

    """ EVENTS ( INPUT )"""
    def keyPressEvent(self, event):
        """
        Todo: Uniforms
            why do uniforms just explode...
        """
        wasd = [Qt.Key_W, Qt.Key_A, Qt.Key_S, Qt.Key_D]
        translation_amount = 0.01
        if event.key() in wasd:
            # self.makeCurrent()
            if event.key() == Qt.Key_W:
                self.uniforms['translation'].data[1] += translation_amount
            if event.key() == Qt.Key_A:
                self.uniforms['translation'].data[0] -= translation_amount
            if event.key() == Qt.Key_S:
                self.uniforms['translation'].data[1] -= translation_amount
            if event.key() == Qt.Key_D:
                self.uniforms['translation'].data[0] += translation_amount

            # upload data
            self.makeCurrent()
            self.uniforms['translation'].uploadData()
            self.doneCurrent()

            # redraw
            self.redraw(clear=True)

        if event.key() == Qt.Key_Q:
            self.uniforms['translation'].data = [0.25, 0.25, 0.0]

            # upload data
            self.makeCurrent()
            self.uniforms['translation'].uploadData()
            self.doneCurrent()

            # redraw
            self.redraw(clear=True)

            #self.update()

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

    def mousePressEvent(self, event):
        from qtpy.QtGui import QCursor
        # relative to window
        print('pos ==', event.pos())

        # relative to display
        print('cursor ==', QCursor.pos())

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
            vertex_source_code = OpenGLWidget.VERTEX_SHADER_DEFAULT
        # fragment shader
        if not fragment_source_code:
            fragment_source_code = OpenGLWidget.FRAGMENT_SHADER_DEFAULT

        # CREATE SHADERS
        vertex_shader = OpenGLWidget.initializeShader(vertex_source_code, GL_VERTEX_SHADER)
        fragment_shader = OpenGLWidget.initializeShader(fragment_source_code, GL_FRAGMENT_SHADER)

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
    widget = OpenGLWidget()
    widget.show()

    # colors = [
    #     [1.0, 0.5, 0.5],
    #     [0.5, 1.0, 0.5],
    #     [0.5, 0.5, 1.0]
    # ]
    #
    # # CREATE PRIMITIVES
    # points = [
    #     [0.8, 0.8, 0.0],
    #     [0.8, 0.2, 0.0],
    #     [0.2, 0.2, 0.0]
    # ]
    # triangle0 = widget.createPolygon(points, colors_list=colors)
    #
    # points = [
    #     [-0.4, -0.4, 0.0],
    #     [-0.8, -0.2, 0.0],
    #     [-0.2, -0.2, 0.0]
    #
    # ]
    # triangle1 = widget.createPolygon(points, colors_list=colors)
    #
    # # polygon
    # points = [
    #     [-0.5, 0.5, 0.0],
    #     [-0.8, 0.8, 0.0],
    #     [-0.2, 0.8, 0.0],
    # ]

    # poly = widget.createPolygon(points, colors_list=colors)
    # why did they detach the shader?
    # will need to shaders from program?
    # glDetachShader(program, vertex)
    # glDetachShader(program, fragment)

    glPointSize(10)
    step = 0.01
    for x in list(numpy.arange(0, 1, step)):
        for y in list(numpy.arange(0, 1, step)):
            points = [
                [x, y, 0.0],
                [x+step, y, 0.0],
                [x, y+step, 0.0]
                ]

            widget.createPolygon(points, colors_list=points)
            print('====')
            print (points)
    from OpenGL.GL import GL_TRIANGLES
    widget.setDrawType(GL_TRIANGLES)
    widget.setDrawStride(3)
    widget.update(draw_stride=3)

    app.exec_()