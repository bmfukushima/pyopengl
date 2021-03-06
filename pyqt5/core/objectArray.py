import numpy

from OpenGL.GL import *


class ObjectArray(object):
    """
    This class contains all of the bindings for one VAO

    Args:
        bind (bool): Determines if the VAO should be bound during the construction...
            this will auto bind if init_data is provided.
    Properties:
        attributes (dict): List of all of the attributes on this VAO
            {attr_name: ObjectArrayAttribute}
        init_data (dict): Data to be uploaded as VBO's to the GPU for
            This specific VAO.  This data should be compiled as a dict like:
                {attr_name: {data_type: int | float | vec2 | vec3 | vec 4, data:[]}
            Note:
                * if this is used, you will need to provide the program to this
                objects constructor
                * requires key of "data_type" with a standard data type from above
        program (glProgram): current program to use.  Only needed if init_data is provided
        vao (Vertex Array): This objects main vertex array
    """

    def __init__(self, attributes=None, bind=True, init_data=None, program=None):
        # generate VAO
        self.vao = glGenVertexArrays(1)

        # bind VAO
        if bind:
            glBindVertexArray(self.vao)

        # init global attrs list/dict
        if attributes:
            self.attributes = attributes
        else:
            self.attributes = {}

        # setup default args
        if init_data:
            glBindVertexArray(self.vao)
            for attr_name in init_data:
                data = init_data[attr_name]["data"]
                data_type = init_data[attr_name]["data_type"]
                self.createAttribute(data, data_type, attr_name, program)

    def createAttribute(self, data, data_type, name, program):
        """
        Creates an attribute and stores it in a VBO

        Args:
            data (scalar/array):
            data_type (str):
                int | float | vec2 | vec3 | vec 4
            name (string):
            program (glProgram): current program
        """
        # bind this object as the current VAO
        glBindVertexArray(self.vao)

        # create attribute
        #attribute = ObjectArrayAttribute(data, data_type, name, program)
        attribute = Attribute(data_type, data)
        attribute.associateReference(program, name)
        # add attribute to registry
        self.attributes[name] = attribute

        # return attribute
        return attribute


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


