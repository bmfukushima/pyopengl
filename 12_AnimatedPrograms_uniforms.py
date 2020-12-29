from math import sin

from OpenGL.GL import (
    glUseProgram, glDrawArrays, glGenVertexArrays, glBindVertexArray,
    glPointSize, glLineWidth,
    GL_POINTS, GL_LINE_LOOP, GL_TRIANGLE_FAN, GL_TRIANGLES,
    glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, glClearColor
)

from core.base import Base
from core.utils import Utils
from core.attribute import Attribute
from core.uniform import Uniform



"""
1.) Vertex/Fragment Shader
2.) Create Attribute
"""
class Test(Base):
    vertex_source = """
    // I/O
    in vec3 position;
    uniform vec3 translation;

    // MAIN FUNCTION
    void main()
    {
        vec3 pos = position + translation;
        gl_Position = vec4(pos, 1.0);
    }    
    """
    fragment_source = """
    // IO
    uniform vec3 base_color;
    
    // MAIN
    void main()
    {
        gl_FragColor = vec4(base_color, 1.0);
    }
    """

    def initialize(self):
        # setup program
        self.program = Utils.initializeProgram(Test.vertex_source, Test.fragment_source)

        # create vertex array (note in 4.5 this call can be glCreateVertexArray(n)
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)

        # ATTRIBUTES
        # set up position
        pos_data = [
            [0.2, 0.2, 0.0],
            [0.2, 0.8, 0.0],
            [0.8, 0.8, 0.0]
        ]

        pos_attr = Attribute("vec3", pos_data)
        pos_attr.associateReference(self.program, "position")
        self.vertex_count = len(pos_data)

        # UNIFORMS
        # translation Down
        self.translation0 = Uniform("vec3", [-0.5, 0.0, 0.0])
        self.translation0.locateVariable(self.program, "translation")

        # translation UP
        self.translation1 = Uniform("vec3", [0.5, 0.0, 0.0])
        self.translation1.locateVariable(self.program, "translation")

        # COLOR R
        self.base_color0 = Uniform("vec3", [1.0, 0.0, 0.0])
        self.base_color0.locateVariable(self.program, "base_color")

        # COLOR G
        self.base_color1 = Uniform("vec3", [0.0, 1.0, 0.0])
        self.base_color1.locateVariable(self.program, "base_color")

    def update(self):
        # RENDER SETTINGS
        glUseProgram(self.program)
        glClearColor(0.5, 0.5, 1.0, 1.0)

        # TRIANGLE 0 | dynamic movement
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.translation0.data[1] += 0.01
        #self.translation0.data[1] *= 5
        if 1 < self.translation0.data[1]:
            self.translation0.data[1] -= 2

        # TRIANGLE 0
        self.translation0.uploadData()
        self.base_color0.uploadData()
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)

        # TRIANGLE 1 | DYNAMIC UPDATES
        self.base_color1.data[2] = sin(self.translation0.data[1])

        # TRIANGLE 1
        self.translation1.uploadData()
        self.base_color1.uploadData()
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)


Test().run()