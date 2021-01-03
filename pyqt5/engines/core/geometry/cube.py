from .geometry import Geometry
from core.utils import Attribute


class Cube(Geometry):
    """
    Args:
        width (int):
        height (int):
        depth (int):
    """
    def __init__(self, width=1, height=1, depth=1):
        super().__init__()

        p0 = [-width/2, -height/2, -depth/2]
        p1 = [ width/2, -height/2, -depth/2]
        p2 = [-width/2,  height/2, -depth/2]
        p3 = [ width/2,  height/2, -depth/2]
        p4 = [-width/2, -height/2,  depth/2]
        p5 = [ width/2, -height/2,  depth/2]
        p6 = [-width/2,  height/2,  depth/2]
        p7 = [ width/2,  height/2,  depth/2]

        # colors for faces in order :
        #       +x | -x | +y | -y | +z | -z
        c0, c1 = [1, 0, 0], [0.5, 0.0, 0.0]
        c2, c3 = [0, 1, 0], [0.0, 0.5, 0.0]
        c4, c5 = [0, 0, 1], [0.0, 0.0, 0.5]

        points = [
            p5, p1, p3, p5, p3, p7,
            p0, p4, p6, p0, p6, p2,
            p6, p7, p3, p6, p3, p2,
            p0, p1, p5, p0, p5, p4,
            p4, p5, p7, p4, p7, p6,
            p1, p0, p2, p1, p2, p3
        ]

        colors =  [c0] * 6   \
                + [c1] * 6   \
                + [c2] * 6   \
                + [c3] * 6   \
                + [c4] * 6   \
                + [c5] * 6   \


        self.attributes["vertex_position"] = Attribute("vec3", points)
        self.attributes["vertex_color"] = Attribute("vec3", colors)

        # setup initial vertex count (required for renderer)
        self.vertexCount()