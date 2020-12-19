from OpenGL import GL

class Utils(object):

    @staticmethod
    def initializeShader(shaderCode, shaderType):
        extension = "#extension GL_ARB_shading_language_420pack: require \n"
        shader_code = "#version 130 \n" + extension + shaderCode

        # create the shader
        shader = GL.glCreateShader(shaderType)

        # link shader code
        GL.glShaderSource(shader, shader_code)

        # compile shader
        GL.glCompileShader(shader)

        # check shader
        compile_success = GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS)

        # if shader fails
        if not compile_success:
            # get error message
            error_message = GL.glGetShaderInfoLog(shader)

            # delete shader
            GL.glDeleteShader(shader)

            # decode error message from bit to utf-8
            error_message = "\n" + error_message.decode("utf-8")

            raise Exception(error_message)

        # shader successful compilation
        return shader

    @staticmethod
    def initializeProgram(vertex_source_code, fragment_source_code):

        ## CREATE PROGRAM
        # compile shaders and store reference
        vertex_shader = Utils.initializeShader(vertex_source_code, GL.GL_VERTEX_SHADER)
        fragment_shader = Utils.initializeShader(fragment_source_code, GL.GL_FRAGMENT_SHADER)

        # create new program
        program = GL.glCreateProgram()

        # attach shaders to program
        GL.glAttachShader(program, vertex_shader)
        GL.glAttachShader(program, fragment_shader)

        # link vertex/fragment shaders together
        GL.glLinkProgram(program)

        ## ERROR CHECKING
        success = GL.glGetProgramiv(program, GL.GL_LINK_STATUS)
        if not success:
            # get error message
            message = GL.glGetProgramInfoLog(program)

            # delete program
            GL.glDeleteProgram(program)

            # convert error message from bit --> utf-8
            message = "\n" + message.decode("utf-8")

            # print error message
            raise Exception(message)

        ## FINISH ERROR CHECKING
        return program