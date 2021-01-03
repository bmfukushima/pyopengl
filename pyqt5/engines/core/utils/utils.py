from OpenGL.GL import *


class Utils(object):

    @staticmethod
    def initializeShader(shaderCode, shaderType):
        extension = "#extension GL_ARB_shading_language_420pack: require \n"
        shader_code = "#version 130 \n" + extension + shaderCode

        # create the shader
        shader = glCreateShader(shaderType)

        # link shader code
        glShaderSource(shader, shader_code)

        # compile shader
        glCompileShader(shader)

        # check shader
        compile_success = glGetShaderiv(shader, GL_COMPILE_STATUS)

        # if shader fails
        if not compile_success:
            # get error message
            error_message = glGetShaderInfoLog(shader)

            # delete shader
            glDeleteShader(shader)

            # decode error message from bit to utf-8
            error_message = "\n" + error_message.decode("utf-8")

            raise Exception(error_message)

        # shader successful compilation
        return shader

    @staticmethod
    def initializeProgram(vertex_source_code, fragment_source_code):

        ## CREATE PROGRAM
        # compile shaders and store reference
        vertex_shader = Utils.initializeShader(vertex_source_code, GL_VERTEX_SHADER)
        fragment_shader = Utils.initializeShader(fragment_source_code, GL_FRAGMENT_SHADER)

        # create new program
        program = glCreateProgram()

        # attach shaders to program
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)

        # link vertex/fragment shaders together
        glLinkProgram(program)

        ## ERROR CHECKING
        success = glGetProgramiv(program, GL_LINK_STATUS)
        if not success:
            # get error message
            message = glGetProgramInfoLog(program)

            # delete program
            glDeleteProgram(program)

            # convert error message from bit --> utf-8
            message = "\n" + message.decode("utf-8")

            # print error message
            raise Exception(message)

        ## FINISH ERROR CHECKING
        return program
