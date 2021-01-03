from .main_mat import MainMaterial
from OpenGL.GL import *


class MeshMaterial(MainMaterial):
    """
    Settings:
        draw_style:
            # TODO setup more draw styles??
            GL_TRIANGLES | TRIANGLE_STRIP? TRIANGLE_FAN? ETC
        double_side (bool): if True
        wireframe (bool): if True
        width (int): if wireframe is True
    """
    def __init__(self, properties={}):
        super().__init__()

        # default settings
        self.settings["draw_style"] = GL_TRIANGLES
        self.settings["double_side"] = False
        self.settings["wireframe"] = False
        self.settings["width"] = 4

        # setup uniforms/settings
        self.updateProperties(properties=properties)

    def updateRenderSettings(self):
        # double sided
        if self.settings["double_side"]:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)

        # wireframe
        if self.settings["wireframe"]:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # line width
        glLineWidth(self.settings["width"])