from OpenGL import GL

from PyQt5.QtGui import QPainter, QColor, QFont

from PyQt5.QtCore import QRect, Qt


class TextLayer(object):
    def drawTextLayer(self):
        painter = QPainter(self)

        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        GL.glPolygonMode(GL.GL_FRONT, GL.GL_FILL)

        painter.beginNativePainting()
        painter.endNativePainting()

        color = QColor().fromRgbF(1.0, 1.0, 1.0, 1.0)
        painter.setPen(color)
        painter.setFont(QFont("Arial", 16))
        #rect = QRect(0, 0, self.width(), self.height())
        # artifacts at min bound?
        rect = QRect(0, 0, self.width(), self.height())
        #painter.drawText(rect, Qt.AlignRight, '%s \n test'%str(self.zoom_factor))
        #print(type(self.zoom_factor), self.zoom_factor)
        painter.drawText(rect, Qt.AlignRight, '{:6.1f}'.format(self.zoom_factor))
        #painter.drawText(rect, Qt.AlignRight, 'hello\nworld\{0}'.format(str(self.zoom_factor)))
