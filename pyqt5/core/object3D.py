"""
todo
    * scale is only setup as uniform
"""

from .matrix import Matrix


class Object3D(object):
    def __init__(self):
        self.transform = Matrix.makeIdentity()
        self.parent = None
        self.children = []

    def addChild(self, child):
        self.children.append(child)
        child.parent = self

    def removeChild(self, child):
        if child in self.children:
            self.children.remove(child)
            child.parent = None
        else:
            raise Exception(child + "not in children... please make better choices with your life")

    def getWorldMatrix(self):
        """
        calculate transformation of this Object3D relative
        to the root Object3D of the scene graph

        Returns (mat4):

        """

        if not self.parent:
            return self.transform
        else:
            return self.parent.getWorldMatrix() @ self.transform

    def getDescendentList(self):
        """
        Returns (list): of all descendents of this object
        """
        descendents = []

        _nodes_to_process = [self]

        while len(_nodes_to_process) > 0:
            # remove first node from list
            node = _nodes_to_process.pop(0)

            # add node to descendents
            descendents.append(node)

            ##   depth first search... order of adding children determines
            ##   the type of search
            # process children
            _nodes_to_process = node.children + _nodes_to_process

        return descendents

    """ TRANSFORMATIONS """
    def applyMatrix(self, matrix, local_coord=True):
        """
        Applies a matrix to this object.
        Args:
            matrix (numpy.array)
            local_coord (bool): determines if this tranformation is in local or world space

        Returns:

        """
        if local_coord:
            self.transform = self.transform @ matrix
        else:
            self.transform = matrix @ self.transform

    def translate(self, x, y, z, local_coord=True):
        matrix = Matrix.makeTranslation(x, y, z)
        self.applyMatrix(matrix, local_coord)

    def rotateX(self, angle, local_coord=True):
        matrix = Matrix.makeRotationX(angle)
        self.applyMatrix(matrix, local_coord)

    def rotateY(self, angle, local_coord=True):
        matrix = Matrix.makeRotationY(angle)
        self.applyMatrix(matrix, local_coord)

    def rotateZ(self, angle, local_coord=True):
        matrix = Matrix.makeRotationZ(angle)
        self.applyMatrix(matrix, local_coord)

    def scale(self, scale, local_coord=True):
        matrix = Matrix.makeScale(scale)
        self.applyMatrix(matrix, local_coord)

    def pos(self):
        #https://numpy.org/doc/stable/reference/generated/numpy.ndarray.item.html
        x = self.transform.item((0, 3))
        y = self.transform.item((1, 3))
        z = self.transform.item((2, 3))

        return [x, y, z]

    def setPos(self, x, y, z):
        # https://numpy.org/doc/stable/reference/generated/numpy.ndarray.item.html
        self.transform.itemset((0, 3), x)
        self.transform.itemset((1, 3), y)
        self.transform.itemset((2, 3), z)

