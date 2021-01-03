#from core.base?
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.geometry.cube import Cube
from core.material.mesh_mat import MeshMaterial

from qtpy.QtWidgets import QOpenGLWidget
from qtpy.QtCore import QTimer


class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(OpenGLWidget, self).__init__(parent)

    def _startTimer(self, fps=60):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)

        self.timer.start(int(1000/fps))

    def initializeGL(self):
        self.renderer = Renderer()
        self.camera = Camera()
        self.scene = Scene()

        geometry = Cube()
        material = MeshMaterial(properties={"use_vertex_color":1})
        self.mesh = Mesh(geometry, material)

        self.scene.addChild(self.mesh)

        self.camera.setPos(0, 0, 4)

        self.paintGL()

    def paintGL(self):
        #self.makeCurrent()
        self.mesh.rotateX(0.0337)
        self.mesh.rotateY(0.0514)
        self.renderer.render(self.scene, self.camera)
        #self.doneCurrent()

        self._startTimer()

        return QOpenGLWidget.paintGL(self)


if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication
    import sys

    app = QApplication([])
    widget = OpenGLWidget()
    widget.show()

    app.exec_()