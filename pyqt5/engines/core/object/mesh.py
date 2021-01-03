from OpenGL.GL import *

from .object3D import Object3D


class Mesh(Object3D):
    def __init__(self, geometry, material):
        super().__init__()

        self.geometry = geometry
        self.material = material

        #
        self.visible = True
        # todo
        """I feel like I was supposed to create/bind a VAO..."""

        # setup associations between attributes in geometry and shader variables
        # a = {"b":"2", "a": "1"}
        # for key, value in a.items():
        #     print(key, value)
        # gen/bind vao
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # associate attr references
        for variable_name, attr_object in geometry.attributes.items():
            attr_object.associateReference(material.program, variable_name)

        # unbind vao
        glBindVertexArray(0)
