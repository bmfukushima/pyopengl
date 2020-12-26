from OpenGL.GL import (
    glUseProgram, glDrawArrays, glGenVertexArrays, glBindVertexArray,
    glPointSize, glLineWidth,
    GL_POINTS, GL_LINE_LOOP, GL_TRIANGLE_FAN, GL_TRIANGLES
)

from core.base import Base
from core.utils import Utils
from core.attribute import Attribute

"""
1.) Vertex/Fragment Shader
2.) Create Attribute
"""
class Test(Base):
    def initialize(self):

        # source code
        vertex_source = """
        in vec3 position;
        in vec3 vertex_color;
        out vec3 color;
        void main()
        {
            gl_Position = vec4(position.x, position.y, position.z, 1.0);
            color = vertex_color;
        }
        """

        fragment_source = """
        in vec3 color;
        void main()
        {
            gl_FragColor = vec4(color.r, color.g, color.b, 1.0);
        }
        """

        # initialize program
        self.program = Utils.initializeProgram(vertex_source, fragment_source)
        glPointSize(20)
        glLineWidth(5)

        self.createTriangle()
        self.createQuad()

    def createTriangle(self):
        # create triangle
        self.tri_vao = glGenVertexArrays(1)
        glBindVertexArray(self.tri_vao)

        # setup vertex attribute
        position_tri_data = [
            [-0.5, 0.8, 0.0],
            [ 0.2, 0.2, 0.0],
            [-0.8, 0.2, 0.0]

        ]
        position_tri_attr = Attribute("vec3", position_tri_data)
        position_tri_attr.associateReference(self.program, "position")
        self.tri_length = len(position_tri_data)

        # setup color attribute
        color_data = [
            [1.0, 0.5, 0.5],
            [0.5, 1.0, 0.5],
            [0.5, 0.5, 0.5]
        ]
        color_data_attr = Attribute("vec3", color_data)
        color_data_attr.associateReference(self.program, "vertex_color")

    def createQuad(self):
        # create quad
        self.quad_vao = glGenVertexArrays(1)
        glBindVertexArray(self.quad_vao)

        # setup vertex attribute
        position_quad_data = [
            [0.8, 0.8, 0.0],
            [0.8, 0.2, 0.0],
            [0.2, 0.2, 0.0],
            [0.2, 0.8, 0.0]

        ]
        position_quad_attr = Attribute("vec3", position_quad_data)
        position_quad_attr.associateReference(self.program, "position")
        self.quad_length = len(position_quad_data)

        # setup color attribute
        color_data = [
            [1.0, 0.5, 0.5],
            [0.5, 1.0, 0.5],
            [0.5, 0.5, 1.0],
            [1.0, 0.5, 1.0]

        ]
        color_data_attr = Attribute("vec3", color_data)
        color_data_attr.associateReference(self.program, "vertex_color")


    def update(self):
        glUseProgram(self.program)

        glBindVertexArray(self.tri_vao)
        glDrawArrays(GL_LINE_LOOP, 0, self.tri_length)

        glBindVertexArray(self.quad_vao)
        glDrawArrays(GL_POINTS, 0, self.quad_length)
        # GL_LINE_LOOP | GL_LINES | GL_TRIANGLES | GL_TRIANGLE_FAN
        """
        # GL_TRIANGLE_FAN
        Starts at index 0, and draws in order of
            ie
                triangle1 = [0, 1, 2]
                triangle2 = [0, 2, 3]
                triangle3 = [0, 3, 4]
        """


Test().run()