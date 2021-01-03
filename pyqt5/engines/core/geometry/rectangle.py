"""
################################################################################
                ####    POINTS    ####
                Assuming origin is at center...
                    * Four vertices grouped into two triangles
                        (p0, p1, p3)
                        (p0, p3, p2)
                    * Assumes knowledge of width/height

    p2                  p3
        |- - - - - /|               p0 = (-w/2 , -h/2)
        |        /  |               p1 = ( w/2 , -h/2)
        |     /     |               p2 = (-w/2 ,  h/2)
        |  /        |               p3 = ( w/2 ,  h/2)
        |/ - - - - -|
    p0                  p1


                ####    COLORS    ####
                    * Colors should be given in the same order as points
                        (c0, c1, c3)
                        (c0, c3, c2)


################################################################################
"""

from core.geometry.geometry import Geometry
from core.attribute import Attribute


class Rectangle(Geometry):
    """

    Args:
        width (int)
        height (int)
    """
    def __init__(self, width=1, height=1):
        super().__init__()

        # points
        p0 = [-width/2, -height/2, 0]
        p1 = [ width/2, -height/2, 0]
        p2 = [-width/2,  height/2, 0]
        p3 = [ width/2,  height/2, 0]

        points_list = [
            p0, p1, p2,
            p0, p3, p2
        ]

        self.attributes["vertex_position"] = Attribute("vec3", points_list)

        # colors
        c0 = [1, 1, 1]
        c1 = [1, 0, 0]
        c2 = [0, 1, 0]
        c3 = [0, 0, 1]

        colors_list = [
            c0, c1, c2,
            c0, c3, c2
        ]

        self.attributes["vertex_color"] = Attribute("vec3", colors_list)

        # setup initial vertex count (required for renderer)
        self.vertexCount()