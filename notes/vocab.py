"""
Raster (array): of pixels, a 1920x1080 image is an array of length 1920x1080
Buffer (data/memory buffer): Memory that serves as temp storage for data while being moved
Frame Buffer (container): Stores pixel related data
	|-- Color Buffer
	|	    stores rgb values
	|-- Depth Buffer
	|	    distance from points on scene to camera
	|-- Stencil Buffer
		    shadows / reflections / etc

Vertex Array Object
    |-* Vertex Buffer Objects
        |-* Vertex Buffer Attributes

Vertex Shader
    - Primary purpose is to determine FINAL position
        Model (transform/scale/rotate)
        View (camera)
        Projection (perspective)
    - Run on EACH vertex

Fragment Shader
    - Depth
        Compares to fragment at same pixel to determine what should be used in the color buffer
    - Transparency
        Rendering order matters
        Opaque
        Transparent Farthest from camera
        Transparent Closest to camera


"""
