from .object3D import Object3D
from core.utils import Matrix
from numpy.linalg import inv


class Camera(Object3D):
    def __init__(self, angle_of_view=60, aspect_ratio=1, near=0.1, far=100):
        super().__init__()
        self.projection_matrix = Matrix.makePerspective(
            angle_of_view, aspect_ratio, near, far)

        self.view_matrix = Matrix.makeIdentity()

    def updateViewMatrix(self):
        """Calculate inverse of transform matrix"""
        self.view_matrix = inv( self.getWorldMatrix())