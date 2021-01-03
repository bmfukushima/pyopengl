from core.utils import Utils
from core.utils import Uniform


class AbstractMaterial(object):
    """

    Args:
        vertex_shader (GLSL): string of GLSL vertex shader code
        fragment_shader (GLSL): string of GLSL fragment shader code

    Properties:
        uniforms (dict): of uniform attrs
            defaults:
                model_matrix | view_matrix | proj_matrix
            {uniform_name: Uniform}
        settings (dict): of settings
            defaults:
                draw_style
            {setting_name: value}
    """
    def __init__(self, vertex_shader=None, fragment_shader=None):

        self.program = Utils.initializeProgram(vertex_shader, fragment_shader)

        # uniforms
        self.uniforms = {}
        self.uniforms['model_matrix'] = Uniform("mat4", None)
        self.uniforms['view_matrix'] = Uniform("mat4", None)
        self.uniforms['proj_matrix'] = Uniform("mat4", None)

        # OpenGL Render Settings
        self.settings = {}
        self.settings["draw_style"] = None

    def initUniforms(self):
        """
        Initialize all uniform variable references
        """
        for name, uniform in self.uniforms.items():
            uniform.locateVariable(self.program, name)

    def updateRenderSettings(self):
        """ Update OpenGL Settings"""
        pass

    def updateProperties(self, properties={}):
        """
        Updates uniforms and/or settings based off of dict provided

        Args:
            properties (dict): of uniforms/settings
                uniforms as:
                    {uniform_name: Uniform}
                settings as:
                    {setting_name: value}
        """
        for name, data in properties.items():
            if name in self.uniforms.keys():
                self.uniforms[name].data = data
            elif name in self.settings.keys():
                self.settings[name] = data
            else:
                raise Exception("material has no property {name}".format(name=name))