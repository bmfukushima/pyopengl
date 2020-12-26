"""
Draw Types (GL_DRAWTYPE):
    GL_POINTS | GL_LINE | GL_LINE_LOOP | GL_TRIANGLE | GL_TRIANGLE_FAN
    GL_LINE_LOOP: Connects the indexes in sequence
        0 --> 1 --> 2 --> 3
    GL_LINES: Connects the indexes as lines
        0 --> 1
        2 --> 3
        4 --> 5
    GL_TRIANGLES: Connects in batches of 3 indexes to form a triangle
        | <--> 1         | <--> 4
        0      |         3      |
        | <--> 2         | <--> 5
    GL_TRIANGLE_FAN: Connects indexes to 0th index in the form of a triangle/fan
        | <-- -- -- -- -- --> 7
        | <-- -- -- -- --> 6
        | <-- -- -- --> 5
        | <-- -- --> 4
        | <-- --> 3
        | <--> 2
        | < 1
        0


    GL_POLYGON?

Fragment (array): of pixels that form a triangle/primitive of arbitrary size (image coordinates).

    Fragments are created during the rasterization process, and can be discarded.
    For each pixel, only one fragment will make it to the Frame Buffer (One pixel
    can contain multiple Fragments, even from the same primitive)

    Usually take fragments based off of depth buffer.
Fragment Shader (shader): code that is run on each individual fragment that is created during
    the rasterization process.
    - Color
    - Depth
        Compares to fragment at same pixel to determine what should be used in the color buffer
    - Transparency
        Rendering order matters
        Opaque
        Transparent Farthest from camera
        Transparent Closest to camera
Frame Buffer (array): Stores pixel related data
	|-- Color Buffer
	|	    stores rgb values
	|-- Depth Buffer
	|	    distance from points on scene to camera
	|-- Stencil Buffer
		    shadows / reflections / etc
Precision (bit depth): the number of bits used in each pixel
    ie. 8 bit = 2^8 = 256 possible colors
Raster (array): of pixels, a 100x100 image is an array of length 10,000
Rasterization (process): of determining which pixels correspond to which
    points/vertexes during the rendering process
Rendering (process): of generating a 2D image from a 3D scene
Shader (process): that is run on GPU (aka a function/program)

Vertex Array Object
    A way to setup reusable templates for Vertex Buffers Layouts
    |-* Vertex Buffer Objects
    |       |-* Vertex Attributes
    |-- Texture Buffer Objects
            |-* Texture Attributes?

Vertex:
    color | pos | normals | etc

Vertex Buffer (data/memory buffer): Memory that serves as temp storage for data while being moved.
    - Can be considered just a buffer which stores as an array of arbitrary data.
            ie. A buffer of a 10x10 image would be an array of size 100.
    - Each individual portion/type of data in the buffer is called an attribute
            ie. {points}{normals}{colors}
            ie. vertexBuffer = [[attr1], [attr2], [att3]]
        the order of operations of the attributes is called the
        VERTEX ATTRIBUTE LAYOUT and can be defined with the <glVertexAttribPointer> call

Vertex Attribute (array): of arbitrary data such as color/pos/normals/etc which
    is stored in a vertex buffer

    To create a Vertex Attribute:
        1.) create variable reference
                variable_ref = glGetAttribLocation(program, attr_name)
        2.) create pointer to data
                glVertexAttribPointer((variable_ref, 1, GL_INT, False, 0, None)
        3.) stream data from pointer to the GPU
                glEnableVertexAttribArray(variable_ref)

Vertex Attribute Layout
    Order that the individual attributes in a single vertex are laid out

    glVertexAttribPointer (array): returns an int that returns the index of
        where the data provided starts
        define an array of generic vertex attribute data
        stride (int): of how many bytes between individual vertex's in a single attribute
                ie. point = [[0.0, 1.0],
                             [1.0, 2.0]]
                    then the stride would be the length of one point in bytes
                            ie. 8 bytes (float = 4 bytes, and 2 floats = 8 bytes)
                        or
                    length_of_point = len(point[0])
                    point_size = length_of_point * sizeof(float)
        pointer (int): offset between individual attributes, in a vertex
            ie if attr = [[xpos, ypos, uvx, uvy],
                          [0.0 , 1.0 , 0.5, 0.5],
                          [1.0 , 2.0 , 3.0, 4.0]]
                then the pointer would be 8, as you need to travel 8 bytes into each
                vertex in order to start he UV coordinates
            cpp --> (const void*)8


Vertex Shader
    - Primary purpose is to determine FINAL position
        Model (transform/scale/rotate)
        View (camera)
        Projection (perspective)
    - Run on EACH vertex


"""
