from .abstract_mat import AbstractMaterial
from .line_mat import LineMaterial
from .main_mat import MainMaterial
from .mesh_mat import MeshMaterial
from .point_mat import PointMaterial

"""
abstract_mat --> AbstractMaterial(object)
    Args:
        vertex_shader (GLSL): string of GLSL vertex shader code
        fragment_shader (GLSL): string of GLSL fragment shader code
    Properties
        program = core.utils.Utils.initializeProgram(vertex_shader, fragment_shader)

        # uniforms
        uniforms = {}
        uniforms['model_matrix'] = core.utils.Uniform("mat4", None)
        uniforms['view_matrix'] = core.utils.Uniform("mat4", None)
        uniforms['proj_matrix'] = core.utils.Uniform("mat4", None)

        # OpenGL Render Settings
        settings = {}
        settings["draw_style"] = None
            # GL_POINTS | GL_TRIANGLES | TRIANGLE_STRIP? TRIANGLE_FAN? ETC

line_mat --> LineMaterial(MainMaterial)
    Args:
        properties (dict)
    Properties
        self.settings["draw_style"] = GL_LINE_STRIP | GL_LINE_LOOP | GL_LINES
        self.settings["type"] = "connected"
        self.settings["width"] = 4

main_mat --> MainMaterial(MainMaterial)
    Args:
        vertex_shader (GLSL): string of GLSL vertex shader code
        fragment_shader (GLSL): string of GLSL fragment shader code
    
    Properties:
        uniforms["base_color"] = Uniform("vec3", [1.0, 1.0, 1.0])
        uniforms["use_vertex_color"] = Uniform("bool", 0)

mesh_mat --> MeshMaterial(MainMaterial)
    Args:
        properties (dict)
    Properties
        settings["draw_style"] = GL_TRIANGLES | TRIANGLE_STRIP | TRIANGLE_FAN
        settings["double_side"] = False
        settings["wireframe"] = False
        settings["width"] = 4

point_mat --> PointMaterial(MainMaterial)
    Args:
        properties (dict)
    Properties
        self.settings["draw_style"] = GL_POINTS
        self.settings["size"] = 8
        self.settings["smooth"] = True
"""