## DATA TYPES
"""
    bool
    int
    float
    vec2/3/4
        array access
            vec4 = (1, 2, 3, 4)
            x == vec4.x == vec4[0]
    mat2/3/4
"""


## MAIN FUNCTION
"""
* Shaders must contain main functions
    This is written in a c-style syntax

void main()
{
    // comment
}
"""


## VERTEX BUFFERS
"""
#### buffers
glGenBuffers(count)
    where do these arbitrary buffers come from?  Just makes a new one?
    is this just instantiating a new buffer on the GPU?
glBindBuffer(bind_target, buffer)
glBufferData(bind_target, buffer_data, buffer_usage)

#### attributes
glGetAttribLocation (program_ref, variable_name): Returns an AttributeReference named <variable_name>
    program_ref (program): program that has the attribute variable
    variable_name(string?)
    returns AttributeReference
glVertexAttribPointer (variable_ref, size, base_type, normalize, stride, offset)
    variable_ref (AttributeReference): to receive data from the Vertex Buffer 
        This should be instantiated with the glGetAttribLocation call
glEnableVertexAttrib(variable_ref): enables the attribute

"""

"""
Overview

Passing data between stages of the pipeline
* Uses TYPE MODIFIERS
    type modifiers are essentially hard coded keyword args which are used to pass arbitrary
    data between steps in the Graphics Pipeline

    in (vertex): values supplied from a BUFFER
    in (fragment): values supplied from VERTEX SHADER

    out (vertex): values supplied to FRAGMENT SHADER
    out (fragment): values stored in color buffer (color, depth, stencil)
    outputs MUST define specific outputs for VERTEX/FRAGMENT shaders
        Vertex
            gl_Position = vec4(0.0, 0.0, 0.0, 1.0)
        Fragment
            gl_FragColor = vec4(0.5, 0.5, 0.5, 1.0)
            gl_Depth = ?

"""