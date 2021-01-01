import numpy
from math import sin, cos, tan, pi


class Matrix(object):
    """
    Rotation angles are radians
    """
    @staticmethod
    def makeIdentity():
        """
        Creates a new identity matrix

        returns (4x4 matrix)
            a numpy array of floats
        """
        identity = numpy.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]).astype(float)
        return identity

    @staticmethod
    def makeTranslation(x, y, z):
        return numpy.array([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1],
        ]).astype(float)

    @staticmethod
    def makeRotationX(angle):
        c = cos(angle)
        s = sin(angle)
        return numpy.array([
            [1, 0,  0, 0],
            [0, c, -s, 0],
            [0, s,  c, 0],
            [0, 0,  0, 1],
        ]).astype(float)

    @staticmethod
    def makeRotationY(angle):
        c = cos(angle)
        s = sin(angle)
        return numpy.array([
            [ c, 0, s, 0],
            [ 0, 1, 0, 0],
            [-s, 0, c, 0],
            [ 0, 0, 0, 1],
        ]).astype(float)

    @staticmethod
    def makeRotationZ(angle):
        c = cos(angle)
        s = sin(angle)
        return numpy.array([
            [c, -s, 0, 0],
            [s,  c, 0, 0],
            [0,  0, 1, 0],
            [0,  0, 0, 1],
        ]).astype(float)

    @staticmethod
    def makeScale(s):
        return numpy.array([
            [s, 0, 0, 0],
            [0, s, 0, 0],
            [0, 0, s, 0],
            [0, 0, 0, 1]
        ]).astype(float)

    @staticmethod
    def makePerspective(angle_of_view=60, aspect_ratio=1, near=0.1, far=100):
        """
        Args:
            angle_of_view (float):
            aspect_ratio (
            near (float):
            far (float):
        """
        a = angle_of_view * pi/180
        b = (far + near) / (near - far)
        c = 2 * far * near / (near - far)
        d = 1.0 / tan(a/2)
        r = aspect_ratio

        return numpy.array([
            [d/r, 0,  0, 0],
            [ 0 , d,  0, 0],
            [ 0 , 0,  b, c],
            [ 0 , 0, -1, 0]
        ]).astype(float)
