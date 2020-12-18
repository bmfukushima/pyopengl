"""

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


Application Stage
    -

Vertex Array Object
    |-* Vertex Buffer Objects
            |--* Vertex Buffer Attributes

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

Startup --> Main Loop   -->  -->  Shutdown
                 > --> user input     ^
                ^    | --> quit ------^
                ^        | --> Yes
                ^        | --> No --> Update --> Render
                ^--  <--  <--  <--  <--  <--  <--|

"""