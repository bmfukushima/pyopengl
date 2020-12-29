'''
link()
bind()
bindAttributeLocation
enableAttributeArray
setAttributeArray
'''

import sys

from PyQt5.QtGui import (
    QImage, QMatrix4x4, QOpenGLShader,
    QOpenGLShaderProgram, QOpenGLTexture,
    QOpenGLWindow, QPainter, QColor, QFont
)
from PyQt5.QtWidgets import (
    QApplication, QOpenGLWidget, QWidget, QVBoxLayout
)

from PyQt5.QtCore import Qt

from OpenGL import GL


class GLWidget(QOpenGLWindow):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.program = None
        self.texture_list = [
        '/media/plt01/Downloads_web/Briana.png',
        '/media/ssd01/_bmfukushima/project/architecture/japan/yakushijiTemple/ref/Yakushi-ji-16-big.jpg'
        ]

    def initializeGL(self):
        # CREATE POLY
        self.makeObject()

        # GL ATTRS
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_CULL_FACE)
        # enable texture blending
        GL.glEnable(GL.GL_BLEND)
        #GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_ALPHA_TEST)
        GL.glAlphaFunc(GL.GL_GREATER, 0.5)
        #GL.glBlendFunc(GL.GL_ONE, GL.GL_ZERO)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        
        '''
        GL.glBlendFuncSeparate(GL.GL_ONE, GL.GL_ONE_MINUS_SRC_ALPHA,
                    GL.GL_ONE_MINUS_DST_ALPHA, GL.GL_ONE)
        '''
        #glBlendFuncSeparate(GLenum srcRGB​, GLenum dstRGB​, GLenum srcAlpha​, GLenum dstAlpha​)
        '''
        GL.glBlendFuncSeparate(
            GL.GL_SRC_COLOR,
            GL.GL_SRC1_COLOR,
            GL.GL_ONE_MINUS_SRC_ALPHA,
            GL.GL_ONE
        )
        '''
        self.createShader()

    def paintGL(self):
        #clear_color = GL.glColor4f(1.0, 1.0,1.0,1.0)

        GL.glClearColor(1, .18, .18, 0)
        
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        
        m = QMatrix4x4()
        m.ortho(-0.5, 0.5, 0.5, -0.5, 4.0, 15.0)
        m.translate(0.0, 0.0, -10.0)
        self.program.setUniformValue('matrix', m)

        for i, texture in enumerate(self.textures):
            #print(texture)
            #GL.glColor4f(0, 1, 0, 0.5)
            texture.bind()
            #GL.glTexEnvf(GL.GL_TEXTURE_ENV, GL.GL_TEXTURE_ENV_MODE,GL.GL_MODULATE)
            GL.glDrawArrays(GL.GL_TRIANGLE_FAN, i*4, 4)
        
        GL.glBegin(GL.GL_TRIANGLES)
        GL.glVertex3f(.25, .25, -.05)
        GL.glVertex3f(.25, -.25, -.05)
        GL.glVertex3f(-.25, -.25, -.05)
    
        GL.glEnd()
        #GL.glPolygonMode(GL.GL_FRONT, GL.GL_FILL)
        #widget = QWidget(self)
        '''
        painter = QPainter(self)

        painter.beginNativePainting()
        painter.endNativePainting()

        color = QColor().fromRgbF(1.0, 1.0, 1.0, 1.0)
        painter.setPen(color)
        painter.setFont(QFont("Arial", 16))
        painter.drawText(0,0,self.width(), self.height(), Qt.AlignRight, 'fuck')
        painter.end()
        '''

    def resizeGL(self, width, height):
        side = min(width, height)
        GL.glViewport(
            (width - side) // 2,
            (height - side) // 2,
            side,
            side
        )

    def makeObject(self):
        self.texCoords = []
        self.vertices = []
        self.textures = []
        coords = (
            (( -.5, +.5, -.5), ( +.5, +.5, -.5), ( +.5, -.5, -.5), ( -.5, -.5, -.5)),
            (( -1, +1, -1), ( +1, +1, -1), ( +1, -1, -1), ( -1, -1, -1))
        )
        for index, texture in enumerate(self.texture_list):
            
            print(-1 - index, texture)
            #coords = ( -1, +1, -1 - index), ( +1, +1, -1 - index), ( +1, -1, -1 - index), ( -1, -1, -1 - index)

            self.textures.append(QOpenGLTexture(QImage(texture)))
            self.texCoords += [(0, 1), (1, 1), (1,0), (0,0)]

            for i in range(4):
                print(coords[index])
                x, y, z = coords[index][i]
                self.vertices.append((x * 0.5, y* 0.5, z* 0.5))
            print(self.texCoords)

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
    #gl_FragColor = texColor = texture2D(texture, texc.st);
    #vec4 texel = texture(tex0, v_uv);
    #color = vec4(texel.rgb, texel.a);

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = GLWidget()
    window.show()
    sys.exit(app.exec_())