from .abstract_mat import AbstractMaterial
from core.uniform import Uniform


class MainMaterial(AbstractMaterial):
    def __init__(self):
        # Create Shaders
        vertex_shader = """
            uniform vec4 proj_matrix;
            uniform vec4 model_matrix;
            uniform vec4 view_matrix;
            
            in vec3 vertex_position;
            in vec3 vertex_color;
            
            out vec3 color;
            
            void main()
            {
                vec4 position = vec4(vertex_position, 1.0);
                gl_Position = proj_matrix * view_matrix * model_matrix * position;
                color = vertex_color;
            }
        """
        fragment_shader = """
        uniform vec3 base_color;
        uniform bool use_vertex_colors;
        in vec3 color;
        // not sure... if this is how this should work lol
        //out vec4 fragColor;
        
        void main()
        {
            vec4 temp_color = vec4(base_color, 1.0);
            
            if ( use_vertex_colors )
                temp_color *= vec4(color, 1.0);
                
            gl_FragColor = temp_color;
        }
        """

        # initialize material
        super().__init__(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        self.uniforms["base_color"] = Uniform("vec3", [1.0, 1.0, 1.0])
        self.uniforms["use_vertex_color"] = Uniform("bool", 0)

        self.initUniforms()