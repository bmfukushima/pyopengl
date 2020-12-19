
#############################
#        HIGH LEVEL
#############################
""" Overview

1.) Create Display Window
2.) Process Geometry
3.) Rasterize
4.) Render
5.) Repeat 2-4 until quit

Startup --> Main Loop   -->  -->  Shutdown
                 > --> user input     ^
                ^    | --> quit ------^
                ^        | --> Yes
                ^        | --> No --> Update --> Render
                ^--  <--  <--  <--  <--  <--  <--|
"""

""" Details

Application Stage
    Initializing the window where graphics will be displayed
    - Sends data to the GPU

Geometry Processing (vertex shader)
    - Determine position of each vertex of each shape

Rasterization
    - Determines which pixels correspond to the geometric shapes
        that will be rendered

Pixel Processing (program shader)
    determines the color of each pixel in the rendered image.

#############################
    Application Stage
#############################
Needs to create display window for OpenGL, and start the main event loop.

The main event loop is going to handle the lions portion of the OpenGL calls
"""


#############################
#        DATA TRANSFER
#############################
""" Overview

Passing data between stages of the pipeline
* Uses TYPE MODIFIERS
    type modifers are essentially hard coded keyword args

    in (vertex): values supplied from a BUFFER
    in (fragment): values supplied from VERTEX SHADER

    out (vertex): values supplied to FRAGMENT SHADER
    out (fragment): values stored in color buffer (color, depth, stencil)
    outputs MUST define specific outputs for VERTEX/FRAGMENT shaders
        Vertex
            gl_position = vec4(0.0, 0.0, 0.0, 1.0)
        Fragment
            gl_FragColor = vec4(0.5, 0.5, 0.5, 1.0)

"""


#############################
#    GEOMETRY PROCESSING
#############################
"""
## SHADERS
1.) Create Shader
2.) Link source code
3.) Compile source code

source code sent to objects
shader must be compiled
    glCreateShader (shaderType): Creates OpenGL Shader of specified type.
        This is used in the <shaderRef> arg
        GL_VERTEX_SHADER | GL_FRAGMENT_SHADER
    glShaderSource (shaderRef, shaderCode)
    glCompileShader (shaderRef)

## SHADER ERROR CHECKING
* Writing in two languages hard to output results..
glGetShaderiv (shaderRef, shaderInfo)
    shaderInfo (GL_SHADER_TYPE | GL_COMPILE_STATUS)
glGetShaderInfoLog (shaderRef)
glDeleteShader(shaderRef)
"""


#############################
#      SHADER PROGRAMS
#############################
"""
Groups of shaders (Vertex, Tessellation, Geometry, Fragment).  Usually just Vertex + Fragment.

Create Program --> Attach Shaders --> Link Program

glCreateProgram(): returns program
glAttachShader(program)
glLinkProgram(program)
"""


#############################
#        APPLICATIONS
#############################
"""
1.) What program to use
2.) What data to use
3.) Draw Mode

glUseProgram(program)
glDrawArrays(draw_mode, first_index, index_count)
    
glPointSize(size)
"""