from OpenGL.GL import (
    glUseProgram, glDrawArrays, glGenVertexArrays, glBindVertexArray,
    glPointSize, glLineWidth,
    GL_POINTS, GL_LINE_LOOP, GL_TRIANGLE_FAN, GL_TRIANGLES
)

from core.base import Base
from core.utils import Utils
from core.attribute import Attribute


class Test(Base):
    def initialize(self):

        # source code
        vertex_source = """
        in vec3 position;
        void main()
        {
            gl_Position = vec4(position.x, position.y, position.z, 1.0);
        }
        """

        fragment_source = """
        void main()
        {
            gl_FragColor = vec4(0.0, 1.0, 0.0, 1.0);
        }
        """

        # initialize program
        self.program = Utils.initializeProgram(vertex_source, fragment_source)
        glPointSize(20)
        glLineWidth(5)
        # create vao
        vao_ref = glGenVertexArrays(1)
        glBindVertexArray(vao_ref)

        # setup vertex attribute
        position_data = [
            [ 0.8,  0.0, 0.0],
            [ 0.4,  0.6, 0.0],
            [-0.4,  0.6, 0.0],
            [-0.8,  0.0, 0.0],
            [-0.4, -0.6, 0.0],
            [ 0.4, -0.6, 0.0]
        ]
        position_attr = Attribute("vec3", position_data)
        position_attr.associateReference(self.program, "position")

    def update(self):
        glUseProgram(self.program)
        glDrawArrays(GL_LINE_LOOP, 0, 6)
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