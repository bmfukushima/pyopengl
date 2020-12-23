"""
Vertex Buffer (data/memory buffer): Memory that serves as temp storage for data while being moved.
    Can be considered just a buffer which stores as an array of arbitrary data.  A buffer of a 10x10 image would be an array of size 100.
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
    |-* Vertex Buffer Objects
    |       |-* Vertex Attributes
    |-- Texture Buffer Objects
            |-* Texture Attributes?

Vertex Shader
    - Primary purpose is to determine FINAL position
        Model (transform/scale/rotate)
        View (camera)
        Projection (perspective)
    - Run on EACH vertex


"""
