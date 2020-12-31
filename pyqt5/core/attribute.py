import numpy

from OpenGL.GL import (
    glEnableVertexAttribArray,
    glGenBuffers,
    glGetAttribLocation,
    glBindBuffer,
    glBufferData,
    glVertexAttribPointer,
    GL_INT,
    GL_FLOAT,
    GL_ARRAY_BUFFER,
    GL_STATIC_DRAW,
)


# TODO Rewatch video...
# https://www.youtube.com/watch?v=xGIWDgqAJ4Q&list=PLxpdybrffYlPqkCyvvLfvwsaB7CB1r0pV&index=8
class Attribute(object):
    """
    data (array): of arbitrary data
    data_type (string): what type of data is being used
        int | float | vec2 | vec3 | vec 4

    """
    def __init__(self, data_type, data):
        self.data = data
        self.data_type = data_type

        # reference to available buffer in GPU
        self.buffer_res = glGenBuffers(1)

        # upload data
        self.uploadData()

    def uploadData(self):
        """
        Stores data on GPU
        """
        # convert to numpy array
        data = numpy.array(self.data)

        # convert to float32
        data = data.astype(numpy.float32)

        # select buffer used by following functions
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer_res)

        # store data in currently bound buffer
        glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)

    def associateReference(self, program, variable_name):
        """
        Associates a variable in the GPU program with this buffer
        :param program:
        :param variable_name:
        :return:
        """

        # get variable reference
        variable_ref = glGetAttribLocation(program, variable_name)

        # return if no reference found
        if variable_ref == -1: return

        # select buffer to use
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer_res)

        # specify how data will be read
        #   from buffer currently bound to GL_ARRAY_BUFFER
        if self.data_type == "int":
            glVertexAttribPointer(variable_ref, 1, GL_INT, False, 0, None)
        elif self.data_type == "float":
            glVertexAttribPointer(variable_ref, 1, GL_FLOAT, False, 0, None)
        elif self.data_type == "vec2":
            glVertexAttribPointer(variable_ref, 2, GL_FLOAT, False, 0, None)
        elif self.data_type == "vec3":
            glVertexAttribPointer(variable_ref, 3, GL_FLOAT, False, 0, None)
        elif self.data_type == "vec4":
            glVertexAttribPointer(variable_ref, 4, GL_FLOAT, False, 0, None)
        else:
             raise Exception("Unknown data type... {data_type}".format(data_type=self.data_type))

        # indicate data should be streamed to variable from buffer
        glEnableVertexAttribArray(variable_ref)
