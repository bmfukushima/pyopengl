"""

Code from http://www.labri.fr/perso/nrougier/python-opengl/#the-hard-way

"""

import ctypes
import logging

import numpy as np
import OpenGL.GL as gl
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
    def __init__(self, parent=None):
        super(MinimalGLWidget, self).__init__(parent)

    def initializeGL(self):
        """
        Run each time a call to update OpenGL is sent
        :return:
        """
        print ('--> initializeGL')
        program = MinimalGLWidget.initializeProgram(vertex_code, fragment_code)

        # why did they detach the shader?
        # gl.glDetachShader(program, vertex)
        # gl.glDetachShader(program, fragment)

        gl.glUseProgram(program)
        gl.glPointSize(20)

    def paintGL(self):
        print('--> paintGL')
        # draw call
        #gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glDrawArrays(gl.GL_POINTS, 0, 1)

    """ EVENTS """
    def keyPressEvent(self, event):
        print('--> keyPressEvent')

        if event.key() == Qt.Key_Q:
            print ("--> Q Pressed")
            self.testDraw()

    def testDraw(self):
        vertex_code = '''
        attribute vec2 position;
        void main()
        {
          gl_Position = vec4(0.25, 0.0, 0.0, 1.0);
        }
        '''

        fragment_code = '''
        void main()
        {
          gl_FragColor = vec4(1.0, 1.0, 0.0, 1.0);
        }
        '''
        # make this widgets context current
        self.makeCurrent()

        #gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glPointSize(100)
        program = MinimalGLWidget.initializeProgram(vertex_code, fragment_code)

        gl.glUseProgram(program)
        gl.glDrawArrays(gl.GL_POINTS, 0, 1)

        # update
        self.doneCurrent()
        self.update()
        #self.paintGL()

    """ UTILS """
    @staticmethod
    def initializeShader(shaderCode, shaderType):
        extension = "#extension GL_ARB_shading_language_420pack: require \n"
        shader_code = "#version 130 \n" + extension + shaderCode

        # create the shader
        shader = gl.glCreateShader(shaderType)

        # link shader code
        gl.glShaderSource(shader, shader_code)

        # compile shader
        gl.glCompileShader(shader)

        # check shader
        compile_success = gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS)

        # if shader fails
        if not compile_success:
            # get error message
            error_message = gl.glGetShaderInfoLog(shader)

            # delete shader
            gl.glDeleteShader(shader)

            # decode error message from bit to utf-8
            error_message = "\n" + error_message.decode("utf-8")

            raise Exception(error_message)

        # shader successful compilation
        return shader

    @staticmethod
    def initializeProgram(vertex_source_code, fragment_source_code):

        ## CREATE PROGRAM
        # compile shaders and store reference
        vertex_shader = MinimalGLWidget.initializeShader(vertex_source_code, gl.GL_VERTEX_SHADER)
        fragment_shader = MinimalGLWidget.initializeShader(fragment_source_code, gl.GL_FRAGMENT_SHADER)

        # create new program
        program = gl.glCreateProgram()

        # attach shaders to program
        gl.glAttachShader(program, vertex_shader)
        gl.glAttachShader(program, fragment_shader)

        # link vertex/fragment shaders together
        gl.glLinkProgram(program)

        ## ERROR CHECKING
        success = gl.glGetProgramiv(program, gl.GL_LINK_STATUS)
        if not success:
            # get error message
            message = gl.glGetProgramInfoLog(program)

            # delete program
            gl.glDeleteProgram(program)

            # convert error message from bit --> utf-8
            message = "\n" + message.decode("utf-8")

            # print error message
            raise Exception(message)

        ## FINISH ERROR CHECKING
        return program


if __name__ == '__main__':
    app = QApplication([])
    widget = MinimalGLWidget()
    widget.show()
    app.exec_()