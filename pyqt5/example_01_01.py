"""

Code from http://www.labri.fr/perso/nrougier/python-opengl/#the-hard-way

"""

import logging
import numpy
from OpenGL.GL import (
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
from PyQt5.QtGui import QOpenGLWindow
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
    """
    def __init__(self, parent=None, draw_stride=1, draw_type=GL_POINTS):
        super(MinimalGLWidget, self).__init__(parent)

        self._draw_stide = draw_stride
        self._draw_type = draw_type
        # UPDATE PROGRAM

    def createTriangle(self):
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
        # vertex shader

        vertex_shader = """
            in vec3 position;
            void main()
            {
                gl_Position = vec4(position.x, position.y, position.z, 1.0);
            }
        """
        # fragment shader
        fragment_shader = """
            void main()
            {
                gl_FragColor = vec4(0.5, 0.5, 1.0, 1.0);
            }
        """
        # program (fragment, vertex)
        program = MinimalGLWidget.initializeProgram(vertex_shader, fragment_shader)
        self.setProgram(program)

        self.triangle = self.createTriangle()
        # why did they detach the shader?
        # glDetachShader(program, vertex)
        # glDetachShader(program, fragment)

        glUseProgram(self.program())
        glPointSize(20)

    def paintGL(self,):
        """
        Has to be called to send signal to draw to OpenGL?
        :return:
        """
        print('--> paintGL')
        # draw call
        #glClear(GL_COLOR_BUFFER_BIT)
        glDrawArrays(self.drawType(), 0, self.drawStride())

    """ EVENTS """
    def keyPressEvent(self, event):
        print('--> keyPressEvent')

        if event.key() == Qt.Key_Q:
            print ("--> Q Pressed")
            self.update(self.triangle, stride=3, primitive_type=GL_LINE_LOOP)
            #self.testDraw()

    def update(self, vao, stride=1, primitive_type=GL_POINTS, vertex_shader=None, fragment_shader=None):
        self.makeCurrent()

        # UPDATE PROGRAM
        # vertex shader
        if not vertex_shader:
            vertex_shader = """
            in vec3 position;
            void main()
            {
                gl_Position = vec4(position, 1.0);
            }
            """
        # fragment shader
        if not fragment_shader:
            fragment_shader = """
            in vec3 position;
            void main()
            {
                gl_FragColor = vec4(0.5, 0.5, 1.0, 1.0);
            }
            """
        # program (fragment, vertex)
        program = MinimalGLWidget.initializeProgram(vertex_shader, fragment_shader)
        self.setProgram(program)
        glUseProgram(self.program())


        # DRAW CALLS
        # TODO UPDATE
        #vao = self.createTriangle()
        # create triangle
        self.tri_vao = glGenVertexArrays(1)
        glBindVertexArray(self.tri_vao)

        # setup vertex attribute
        position_tri_data = [
            [-0.5, 0.8, 0.0],
            [0.2, 0.2, 0.0],
            [-0.8, 0.2, 0.0]

        ]
        position_tri_attr = Attribute("vec3", position_tri_data)
        position_tri_attr.associateReference(self.program(), "position")
        self.tri_length = len(position_tri_data)


        #glBindVertexArray(vao)
        #glDrawArrays(GL_POINTS, 0, 3)

        # update
        self.doneCurrent()
        # apparently I can provide a region for this?
        self.setDrawType(primitive_type)
        self.setDrawStride(stride)
        return QOpenGLWidget.update(self)

    """ PROPERTIES """
    def program(self):
        return self._program

    def setProgram(self, program):
        self._program = program

    def drawType(self):
        return self._draw_type

    def setDrawType(self, _draw_type):
        self._draw_type = _draw_type

    def drawStride(self):
        return self._draw_stide

    def setDrawStride(self, _draw_stide):
        self._draw_stide = _draw_stide

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
    def initializeProgram(vertex_source_code, fragment_source_code):

        ## CREATE PROGRAM
        # compile shaders and store reference
        vertex_shader = MinimalGLWidget.initializeShader(vertex_source_code, GL_VERTEX_SHADER)
        fragment_shader = MinimalGLWidget.initializeShader(fragment_source_code, GL_FRAGMENT_SHADER)

        # create new program
        program = glCreateProgram()

        # attach shaders to program
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)

        # link vertex/fragment shaders together
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