from .main_mat import MainMaterial
from OpenGL.GL import *


class LineMaterial(MainMaterial):
    """

    Settings:
        draw_style (GL_LINE_TYPE):
            GL_LINE_STRIP | GL_LINE_LOOP | GL_LINES
        type (string):
            connected | loop | segments
        width (int)
    """
    def __init__(self, properties={}):
        super().__init__()

        # default settings
        self.settings["draw_style"] = GL_LINE_STRIP
        self.settings["type"] = "connected"
        self.settings["width"] = 4

        # setup uniforms/settings
        self.updateProperties(properties=properties)

    def updateRenderSettings(self):
        # setup line width
        glLineWidth(self.settings["width"])

        # setup draw style
        if self.settings["type"] == "connected":
            self.settings["draw_style"] = GL_LINE_STRIP
        elif self.settings["type"] == "loop":
            self.settings["draw_style"] = GL_LINE_LOOP
        elif self.settings["type"] == "segments":
            self.settings["draw_style"] = GL_LINES
        else:
            raise Exception("FAIL!!! Need better line type... {line_type} blows, try another one like \n connected | loop | segments \n you noob".format(line_type=self.settings["type"]))

