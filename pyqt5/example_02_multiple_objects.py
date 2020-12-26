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
import numpy
from OpenGL.GL import (
    glDetachShader,
    glEnableVertexAttribArray,
    glGenBuffers,
    glGetAttribLocation,
    glBindBuffer,
    glBufferData,
    glVertexAttribPointer,
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
    GL_INT,
    GL_FLOAT,
    GL_ARRAY_BUFFER,
    GL_STATIC_DRAW,
    GL_POINTS,
    GL_LINE_LOOP,
    GL_COMPILE_STATUS,
    GL_VERTEX_SHADER,
    GL_FRAGMENT_SHADER
)
#import OpenGL as gl
from PyQt5.QtWidgets import QApplication, QOpenGLWidget
from PyQt5.QtGui import QOpenGLWindow, QOpenGLVertexArrayObject
from PyQt5.QtCore import Qt


logger = logging.getLogger(__name__)


vertex_code = '''
attribute vec2 position;
void main()
{
  gl_Position = vec4(0.0, 0.5, 0.0, 1.0);
}
'''


fragment_code = '''
void main()
{
  gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
'''


class MinimalGLWidget(QOpenGLWidget):
    """
    Args:
        draw_stride (int): How many points are in the primitive type to be drawn.

            This sets the glDrawArrays stride value.
        draw_type (GL_DRAW_TYPE):
            GL_POINTS, GL_LINE_LOOP, GL_TRIANGLE_FAN, GL_TRIANGLES

    Notes:
        - update() calls the paintGL function
        - for some reason the paintGL runs twice on init
        - update behavior by default is to clear on paintGL
            use "setUpdateBehavior(PartialUpdate | NoPartialUpdate)"
                PartialUpdate is default
        -
    """
    # vertex shader
    VERTEX_SHADER_DEFAULT = """
            in vec3 position;
            void main()
            {
                gl_Position = vec4(position, 1.0);
            }
            """
    FRAGMENT_SHADER_DEFAULT = """
            void main()
            {
                gl_FragColor = vec4(1.0, 0.5, 1.0, 1.0);
            }
            """

    def __init__(self, parent=None, draw_stride=0, draw_type=GL_POINTS):
        super(MinimalGLWidget, self).__init__(parent)
        self._update_list = []
        self._draw_stride = draw_stride
        self._draw_type = draw_type

        # UPDATE PROGRAM

    # todo move creation of primitives into this
    def createPolygon(self, points_list=[[]]):
        polygon_vao = glGenVertexArrays(1)
        glBindVertexArray(polygon_vao)

        polygon_attr = Attribute("vec3", points_list)
        polygon_attr.associateReference(self.program(), "position")
        return polygon_vao

    def createQuad(self):

        # generate VAO
        quad_vao = glGenVertexArrays(1)

        # bind VAO
        glBindVertexArray(quad_vao)

        position_data = [
            [-0.4, -0.4, 0.0],
            [-0.8, -0.2, 0.0],
            [-0.2, -0.2, 0.0],
            [-0.2, -0.8, 0.0]

        ]
        # create attr
        quad_attr = Attribute("vec3", position_data)
        quad_attr.associateReference(self.program(), "position")
        self.quad_length = 4
        return quad_vao

    def createTriangle(self):
        """
        Creates a VAO of a triangle

        Returns: (VAO)
        """
        # need some sort of object class to track
        # initialize VAO
        triangle_vao = glGenVertexArrays(1)

        # bind VAO to be current
        glBindVertexArray(triangle_vao)

        # setup points
        position_data = [
            [0.8, 0.8, 0.0],
            [0.8, 0.2, 0.0],
            [0.2, 0.2, 0.0]
        ]

        # create attr
        triangle_attr = Attribute("vec3", position_data)
        triangle_attr.associateReference(self.program(), "position")
        self.triangle_length = len(position_data)
        return triangle_vao

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

        self.quad = self.createQuad()
        self.triangle = self.createTriangle()

        # why did they detach the shader?
        # will need to shaders from program?
        #glDetachShader(program, vertex)
        #glDetachShader(program, fragment)

        glPointSize(20)
        #self.update([self.quad, self.triangle], stride=4)
        for object in [self.triangle, self.quad]:
            self.update(
                [object],
                stride=3,
                primitive_type=GL_POINTS
            )
        #self.update([self.triangle], stride=3)

    # def paintGL(self):
    #     print('paint')
    #     pass

    def paintGL(self):
        """
        Has to be called to send signal to draw to OpenGL?
        :return:
        """
        print('--> paintGL')
        # if not self.isValid():
        #     return
        # draw call
        for vao in self._update_list:
            glBindVertexArray(vao)
            glDrawArrays(self.drawType(), 0, self.drawStride())

        return QOpenGLWidget.paintGL(self)

    """ EVENTS """
    def keyPressEvent(self, event):
        print('--> keyPressEvent')

        if event.key() == Qt.Key_Q:
            print ("--> Q Pressed")

            vertex_source = """
                in vec3 position;
                void main()
                {
                    gl_Position = vec4(position.x * 0.5, position.y * 0.5, position.z * 0.5, 1.0);
                }
            """
            fragment_source = """
                void main()
                {
                    gl_FragColor = vec4(0.0, 0.5, 1.0, 1.0);
                }
            """
            # todo only draws second call? the same as before =\
            for object in [self.triangle, self.quad]:
                self.update(
                    [object],
                    stride=3,
                    primitive_type=GL_LINE_LOOP,
                    fragment_source_code=fragment_source,
                    vertex_source_code=vertex_source
                )

            # MinimalGLWidget.initializeProgram(fragment_source_code=fragment_source)
            # test_triangle = self.createTriangle()
            # self.update(test_triangle, stride=3, primitive_type=GL_LINE_LOOP)
            #self.testDraw()

    def update(
            self,
            vao_list,
            stride=1,
            primitive_type=GL_POINTS,
            clear=False,
            vertex_source_code=None,
            fragment_source_code=None
        ):
        # setup draw attrs
        self.setDrawType(primitive_type)
        self.setDrawStride(stride)
        self._update_list = vao_list

        # START STATE UPDATE
        self.makeCurrent()

        # clear
        if clear:
            glClear(GL_COLOR_BUFFER_BIT)

        # update program if new vertex/fragment code is provided
        if vertex_source_code or fragment_source_code:
            program = self.initializeProgram(vertex_source_code=vertex_source_code, fragment_source_code=fragment_source_code)
            self.setProgram(program)
            print('program?')
            # TODO how to set up association?

        # bind VAO
        print('draw????')
        for vao in vao_list:
            glBindVertexArray(vao)
            glDrawArrays(self.drawType(), 0, self.drawStride())
        #glBindVertexArray(vao_list)
        #glDrawArrays(primitive_type, 0, stride)
        # update
        self.doneCurrent()

        # draw
        #self.paintGL()
        return QOpenGLWidget.update(self)
        print('end?')

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

# TODO Rewatch video...
# https://www.youtube.com/watch?v=xGIWDgqAJ4Q&list=PLxpdybrffYlPqkCyvvLfvwsaB7CB1r0pV&index=8
class Attribute(object):
    """
    data (array): of arbitrary data
    data_type (string): what type of data is being used
        int | float | vec2 | vec3 | vec 4

    """
    def __init__(self, data_type, data):
        self.data = data
        self.data_type = data_type

        # reference to available buffer in GPU
        self.buffer_res = glGenBuffers(1)

        # upload data
        self.uploadData()

    def uploadData(self):
        """
        Stores data on GPU
        """
        # convert to numpy array
        data = numpy.array(self.data)

        # convert to float32
        data = data.astype(numpy.float32)

        # select buffer used by following functions
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer_res)

        # store data in currently bound buffer
        glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)

    def associateReference(self, program, variable_name):
        """
        Associates a variable in the GPU program with this buffer
        :param program:
        :param variable_name:
        :return:
        """

        # get variable reference
        variable_ref = glGetAttribLocation(program, variable_name)

        # return if no reference found
        if variable_ref == -1: return

        # select buffer to use
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer_res)

        # specify how data will be read
        #   from buffer currently bound to GL_ARRAY_BUFFER
        if self.data_type == "int":
            glVertexAttribPointer(variable_ref, 1, GL_INT, False, 0, None)
        elif self.data_type == "float":
            glVertexAttribPointer(variable_ref, 1, GL_FLOAT, False, 0, None)
        elif self.data_type == "vec2":
            glVertexAttribPointer(variable_ref, 2, GL_FLOAT, False, 0, None)
        elif self.data_type == "vec3":
            glVertexAttribPointer(variable_ref, 3, GL_FLOAT, False, 0, None)
        elif self.data_type == "vec4":
            glVertexAttribPointer(variable_ref, 4, GL_FLOAT, False, 0, None)
        else:
             raise Exception("Unknown data type... {data_type}".format(data_type=self.data_type))

        # indicate data should be streamed to variable from buffer
        glEnableVertexAttribArray(variable_ref)





if __name__ == '__main__':
    app = QApplication([])
    widget = MinimalGLWidget()
    widget.show()
    app.exec_()