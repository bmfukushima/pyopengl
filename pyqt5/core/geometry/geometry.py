class Geometry(object):
    """

    Properties:
        attributes (dict): of Vertex Attributes
            {name: object}
        vertex_count (int): number of total vertexes
    """
    def __init__(self):
        self.attributes = {}
        self.vertex_count = None

    def vertexCount(self):
        """
        Returns the vertex count.

        The vertex count is the length of any attribute object

        """

        attrib = list(self.attributes.values())[0]

        self.vertex_count = len(attrib)