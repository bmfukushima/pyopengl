

#        HIGH LEVEL
""" Overview

1.) Application (Create Display Window)
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

1.) Vertex Buffer (Buffer, or array of memory)
2.) Convert Buffer to GPU VRAM
3.) Draw from VRAM
"""

""" Details

1.) Application Stage
    - Initializing the window where graphics will be displayed
    - Sends data to the GPU
        Reading data required for rendering and sending to GPU
    - Monitor HW for user input
    - Main Loop

2.) Geometry Processing (vertex shader)
    - Determine position of each vertex of each shape

3.) Rasterization
    - Determines which pixels correspond to the geometric shapes
        that will be rendered

4.) Pixel Processing (program shader)
    determines the color of each pixel in the rendered image.


    Application Stage

Needs to create display window for OpenGL, and start the main event loop.

The main event loop is going to handle the lions portion of the OpenGL calls
"""


#       CLEAR BUFFER
"""
See vocab --> FrameBuffer
"""

#        DATA TRANSFER
""" 
See glsl.py --> TYPE MODIFIERS
"""


#       APPLICATION
"""
CPU Portion before sending to GPU

Creating an application
Base
Renderer
Scene
Camera
Mesh
atleast one geometry class
atleast one material class
"""


#    GEOMETRY PROCESSING
"""
Evaluation of curved surface
Transform, projection
clipping, culling, primitive assembly
Lighting / Colors (per vertex)

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

# layout attributes
# run program
"""


#       RASTERIZATION
"""
for each triangle:
    for fragment in triangle:
        for pixel in fragment:
            pixel_color = color
Which fragments is it going to color
What color is each fragment

Texture 
transformation/projection
mapping
filtering

"""

#      SHADER PROGRAMS
"""
Groups of shaders (Vertex, Tessellation, Geometry, Fragment).  Usually just Vertex + Fragment.

# setup program
Create Program --> Attach Shaders --> Link Program

glCreateProgram(): returns program
glAttachShader(program)
glLinkProgram(program)


# use program
Set extra attrs --> Set Program --> Draw Primitives

glPointSize(size)
glUseProgram(program)
glDrawArrays(draw_mode, first_index, index_count)
"""


#        STATES
"""
- {color: (1.0, 1.0, 1.0, 1.0), xform: 4x4Matrix}
- Can run multiple states in the main loop.
    ie a group of triangles could be running one state, while another group
        of primitvies is running another state.
- Good for storing data for later use.  As states will essentially layer on top of each other
    until the state is overridden.
        Resources
            Fonts | Textures
        Attrs
            Appearance: lights, materials, colors
            Transformation: camera, model, texture
            Options: constant per-frame
            
"""


#       DESIGN DECISIONS
"""
ImmediateMode
Ordered
Has States
Triangle as primitive
Framebuffer
"""

#       ETC
"""
Textures are per fragment
Colors are per vertex
    Lighting conditions wont change over a triangle as it is flat.  So you can do a
    smaller calculation, and then compute the blending average.
"""