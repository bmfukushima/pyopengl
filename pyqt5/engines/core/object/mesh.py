from OpenGL.GL import *

from .object3D import Object3D


class Mesh(Object3D):
    """
    Args:
        geometry (core.geometry.OBJECT):
        material (core.material.MAT):
    Properties:
        visible (bool): determines if this mesh will be shown during updates
        vao (VAO):

    """
    def __init__(self, geometry, material):
        super().__init__()

        # setup default attrs
        self.geometry = geometry
        self.material = material
        self.visible = True
        self.vao = glGenVertexArrays(1)

        # setup associations between attributes in geometry and shader variables
        # bind vao
        glBindVertexArray(self.vao)

        # init/associate attr references
        for variable_name, attr_object in geometry.attributes.items():
            attr_object.associateReference(material.program, variable_name)

        # unbind vao
        glBindVertexArray(0)
