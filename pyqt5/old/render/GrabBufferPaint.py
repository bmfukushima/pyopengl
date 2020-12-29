import sys
import math


from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QCursor, QOpenGLWindow, QOpenGLFramebufferObjectFormat,
    QOpenGLFramebufferObject, QOpenGLPaintDevice, QPainter,
    QImage
)
from PyQt5.QtWidgets import (QApplication)

import OpenGL.GL as gl


class GLWindow(QOpenGLWindow):
    def __init__(self, parent=None):
        super(GLWindow, self).__init__(parent)

    def initializeGL(self):
        gl.glClearColor(0.18, 0.18, 0.18, 1.0)

    def paintGL(self):
        # camera points towards -z axis
        # viewport has coordinates of 1 unit
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        gl.glTranslatef(0, 0, -5)

        # set color
        gl.glColor4f(0, 1, 0, 1)
        # set drawing mode
        gl.glLineWidth(5)
        gl.glPolygonMode(gl.GL_FRONT, gl.GL_LINE)
        gl.glBegin(gl.GL_TRIANGLES)
        gl.glVertex3f(-0.5, -0.5, .5)
        gl.glVertex3f(0, 0.5, .5)
        gl.glVertex3f(0.5, -0.5, .5)

        gl.glVertex3f(-0.25, -0.25, .25)
        gl.glVertex3f(0, 0.25, .25)
        gl.glVertex3f(0.25, -0.25, .25)

        gl.glEnd()

    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        gl.glViewport((width - side) // 2, (height - side) // 2, side, side)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def keyPressEvent(self, event, *args, **kwargs):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == (Qt.AltModifier):
            if event.key() == Qt.Key_A:
                self.getFrameBuffer()
                print ('alt + a')
        elif modifiers == (Qt.AltModifier | Qt.ShiftModifier):
            print ('douuubllel modifieiieir')
        return QOpenGLWindow.keyPressEvent(self, event, *args, **kwargs)

    def getFrameBuffer(self):
        def paintGL():
            #QOpenGLPaintDevice fboPaintDev(width(), height());
            fboPaintDev = QOpenGLPaintDevice(self.width(), self.height())
            #QPainter painter(&fboPaintDev);
            painter = QPainter(fboPaintDev)
            painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing);

            #//now start OpenGL painting
            painter.beginNativePainting();
            """
            gl.glClearColor(0.5, 0.0, 0.0, 1.0);
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT);
            gl.glColor4f(0,1,0,1)
            gl.glPolygonMode(gl.GL_FRONT, gl.GL_LINE)
            gl.glBegin(gl.GL_TRIANGLES)
            gl.glVertex3f(-.1, -.1, -1)
            gl.glVertex3f(.1, 0, -1)
            gl.glVertex3f(-.1, .1, -1)
            gl.glEnd()
            """
            painter.endNativePainting();
            #//draw non-OpenGL stuff with QPainter
            painter.drawText(20, 40, "Foo");

            painter.end();

        '''
        image = self.grabFramebuffer()
        #print(image.hasAlphaChannel())
        #image.convertToFormat(QImage.Format_RGBA8888)
        #print(image.hasAlphaChannel())
        #print(image)
        image.save("/media/ssd01/dev/temp/test2.png")
        #2 WORKS: bind FBO and render stuff with paintGL() call
        '''
        format = QOpenGLFramebufferObjectFormat()
        format.setAttachment(QOpenGLFramebufferObject.CombinedDepthStencil)
        m_fbo = QOpenGLFramebufferObject(self.width(), self.height(), format)
        #gl.resizeGL(width(), height())

        m_fbo.bind()
        paintGL()
        #//You could now grab the content of the framebuffer we've rendered to
        image2 = m_fbo.toImage();
        image2.save("/media/ssd01/dev/temp/test.png")
        m_fbo.release();
        #self.setPixmap(QPixmap.fromImage(image))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = GLWindow()
    pos = QCursor.pos()
    window.show()
    window.setGeometry(pos.x() - 320, pos.y() - 240, 640, 480)
    sys.exit(app.exec_())
