import numpy
from OpenGL.GL import (
    glGetUniformLocation,
    glUniform1i,
    glUniform1f,
    glUniform2f,
    glUniform3f,
    glUniform4f,
    glUniformMatrix4fv,
    GL_TRUE
)


class Uniform(object):
    """
    data (array): of arbitrary data
    data_type (string): what type of data is being used
        int | float | vec2 | vec3 | vec4 | mat4

    """
    def __init__(self, data_type, data):
        self.data = data
        self.data_type = data_type
        self.variable_ref = None

    def locateVariable(self, program, variable_name):
        """
        Get and store reference to uniform variable

        Args:
        program (glProgram):
            variable_name (str): name of this uniform
        """
        self.variable_ref = glGetUniformLocation(program, variable_name)

    def uploadData(self):
        """
        Store data in uniform variable
        """
        # preflight
        if self.variable_ref == -1: return

        if self.data_type == "int":
            glUniform1i(self.variable_ref, self.data)
        elif self.data_type == "bool":
            glUniform1i(self.variable_ref, self.data)
        elif self.data_type == "float":
            glUniform1f(self.variable_ref, self.data)
        elif self.data_type == "vec2":
            glUniform2f(self.variable_ref, *self.data)
        elif self.data_type == "vec3":
            glUniform3f(self.variable_ref, *self.data)
        elif self.data_type == "vec4":
            glUniform4f(self.variable_ref, *self.data)
        elif self.data_type == "mat4":
            glUniformMatrix4fv(self.variable_ref, 1, GL_TRUE, self.data)
        else:
             raise Exception("Unknown data type... {data_type}".format(data_type=self.data_type))
