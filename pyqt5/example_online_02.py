# https://stackoverflow.com/questions/35854076/pyqt5-opengl-4-1-core-profile-invalid-frame-buffer-operation-mac-os
#!/usr/bin/env python

from PyQt5.QtGui import (
        QOpenGLBuffer,
        QOpenGLShader,
        QOpenGLShaderProgram,
        QOpenGLVersionProfile,
        QOpenGLVertexArrayObject,
        QSurfaceFormat,
    )
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget


class QTWithGLTest(QMainWindow):
    """Main window."""

    def __init__(self, versionprofile=None, *args, **kwargs):
        """Initialize with an OpenGL Widget."""
        super(QTWithGLTest, self).__init__(*args, **kwargs)

        self.widget = QOpenGLControllerWidget(versionprofile=versionprofile)
        self.setCentralWidget(self.widget)
        self.show()


class QOpenGLControllerWidget(QOpenGLWidget):
    """Widget that sets up specific OpenGL version profile."""

    def __init__(self, versionprofile=None, *args, **kwargs):
        """Initialize OpenGL version profile."""
        super(QOpenGLControllerWidget, self).__init__(*args, **kwargs)

        self.versionprofile = versionprofile

    def initializeGL(self):
        """Apply OpenGL version profile and initialize OpenGL functions."""
        self.gl = self.context().versionFunctions(self.versionprofile)
        if not self.gl:
            raise RuntimeError("unable to apply OpenGL version profile")

        self.gl.initializeOpenGLFunctions()

        self.createShaders()
        self.createVBO()
        self.gl.glClearColor(0.0, 0.0, 0.0, 0.0)

    def paintGL(self):
        """Painting callback that uses the initialized OpenGL functions."""
        if not self.gl:
            return

        self.gl.glClear(self.gl.GL_COLOR_BUFFER_BIT | self.gl.GL_DEPTH_BUFFER_BIT)
        self.gl.glDrawArrays(self.gl.GL_TRIANGLES, 0, 3)

    def resizeGL(self, w, h):
        """Resize viewport to match widget dimensions."""
        self.gl.glViewport(0, 0, w, h)

    def createShaders(self):
        ...

    def createVBO(self):
        ...


if __name__ == '__main__':
    import sys

    fmt = QSurfaceFormat()
    fmt.setVersion(4, 1)
    fmt.setProfile(QSurfaceFormat.CoreProfile)
    fmt.setSamples(4)
    QSurfaceFormat.setDefaultFormat(fmt)

    vp = QOpenGLVersionProfile()
    vp.setVersion(4, 1)
    vp.setProfile(QSurfaceFormat.CoreProfile)

    app = QApplication(sys.argv)
    window = QTWithGLTest(versionprofile=vp)
    window.show()
    sys.exit(app.exec_())