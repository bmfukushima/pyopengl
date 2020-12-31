from core.base import Base
from core.utils import Utils
from OpenGL import GL


class Application(Base):

    def initialize(self):
        # Create GPU Program

        # vertex shader
        vs_source = """
        void main()
        {
            gl_Position = vec4(0.0, 0.0, 0.0, 1.0); 
        }
        """

        # fragment shader
        fs_source = """
        void main()
        {
            gl_FragColor = vec4(0.5, 0.5, 1.0, 1.0);
        }
        """

        # send to GPU, compile, store program reference
        self.program = Utils.initializeProgram(vs_source, fs_source)

        # set point size
        GL.glPointSize(20)

    def update(self):
        # select program to use
        GL.glUseProgram(self.program)

        # render geometric object(s) using program
        GL.glDrawArrays(GL.GL_POINTS, 0, 1)



Application().run()