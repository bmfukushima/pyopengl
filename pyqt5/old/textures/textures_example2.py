import sys

from PyQt5.QtGui import (
    QImage, QMatrix4x4, QOpenGLShader,
    QOpenGLShaderProgram, QOpenGLTexture
)
from PyQt5.QtWidgets import (
    QApplication, QOpenGLWidget, QWidget, QVBoxLayout
)

from OpenGL import GL


class GLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.program = None

    def initializeGL(self):
        # CREATE POLY
        self.makeObject()

        # GL ATTRS
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_CULL_FACE)
        # enable texture blending
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        self.createShader()

    def paintGL(self):
        GL.glClearColor(.18, .18, .18, 1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        m = QMatrix4x4()
        m.ortho(-0.5, 0.5, 0.5, -0.5, 4.0, 15.0)
        m.translate(0.0, 0.0, -10.0)

        self.program.setUniformValue('matrix', m)

        self.texture.bind()
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, 0, 4)

    def resizeGL(self, width, height):
        side = min(width, height)
        GL.glViewport(
            (width - side) // 2,
            (height - side) // 2,
            side,
            side
        )

    def makeObject(self):
        self.coords = (
            ( -1, +1, -1 ), ( +1, +1, -1 ), ( +1, -1, -1 ), ( -1, -1, -1 )
        )

        self.texCoords = []
        self.vertices = []

        self.texture = QOpenGLTexture(
            QImage('/media/plt01/Downloads_web/Briana.png')
        )

        for i in range(4):
            self.texCoords.append(((i == 0 or i == 3), (i == 0 or i == 1)))
            x, y, z = self.coords[i]
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


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        mainLayout = QVBoxLayout()

        widget = GLWidget()
        widget.setMinimumSize(200, 200)
        mainLayout.addWidget(widget)
        self.setLayout(mainLayout)

        self.setWindowTitle("Textures")


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())