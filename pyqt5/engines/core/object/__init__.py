from .camera import Camera
from .group import Group
from .mesh import Mesh
from .scene import Scene

"""
object3D --> Object3D(object)
    Properties:
        transform = core.utils.Matrix.makeIdentity()
        parent = None
        children = []

camera --> Camera(Object3D)
    Args:
        angle_of_view=60, aspect_ratio=1, near=0.1, far=100
    Properties:
        projection_matrix = core.utils.Matrix.makePerspective(
            angle_of_view, aspect_ratio, near, far)
        view_matrix = Matrix.makeIdentity()

group --> Group(Object3D)

mesh --> Mesh(Object3D)
    Args:
        geometry = core.geometry.GEO
        material = core.material.MAT
    Properties
        visible = True
        vao = glGenVertexArrays(1)

scene --> Scene(Object3D)
"""