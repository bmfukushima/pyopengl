from .main_mat import MainMaterial
from OpenGL.GL import *


class PointMaterial(MainMaterial):
    """
    Settings:
        draw_style (GL_POINTS)
        point_size (int): how large points will be displayed as
        point_smooth (bool): if points are smoothed
    """
    def __init__(self, properties={}):
        super().__init__()

        # default settings
        self.settings["draw_style"] = GL_POINTS
        self.settings["size"] = 8
        self.settings["smooth"] = True

        # setup uniforms/settings
        self.updateProperties(properties=properties)

    def updateRenderSettings(self):
        glPointSize(self.settings["size"])

        if self.settings["smooth"]:
            glEnable(GL_POINT_SMOOTH)
        else:
            glDisable(GL_POINT_SMOOTH)