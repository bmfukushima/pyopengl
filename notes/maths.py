
#       VECTORS
"""
## VOCAB
CAPITAL BOLD = MATRIX
LOWER BOLD = VECTOR

Basis Vectors (vector): using the vectors i=<1,0> and j=<0,1>,
    any vector can be written in terms of these vectors using
    VECTOR ADDITION and SCALAR MULTIPLICATION.
        |- v = <x,y>
            ==> <x,0> + <0,y>
            ==> x * <1,0> + y * <0,1>
            ==> x*i + y*j

    This is one set of BASIS VECTORS, known as the STANDARD BASIS

Dot Product: Given 2 matrixes to multiply, this returns a third matrix, consisting of
    the 2 original multiplied together.  The DOT PRODUCT can return any COLUMN / ROW combination
    given the formula
        Matrix1_ROW + Matrix2_COL
            ie
        [a11, a12]  *   [b11, b12]  =   [<a11, a12> o <b11, b21>, ...]  =   [c11, c12]
        [a21, a22]  *   [b21, b22]  =   [..., <a21, a22> o <b12, b22>]  =   [c21, c22]


Linear Transformation (function): a function is considered to be a linear transformation if
    the following two conditions are met:
        LEGEND:
            c = scalar
            v/w = vectors
            F = function
        1.) Scalar Multiplication
            F(c * v) = c * F(v)
        2.) Vector Addition
            F(w + v) = F(w) + F(v)

Points (coordinates): position in space

Scalar (number): singular number
    Multiplication:
        scalar * vector = vector
            |- <s*v1, s*v2>
            |- 2 * <2,3> = <4,6>
            |- direction reversed when scalar is negative
                    positive --> top right
                    negative --> bot left

Vector (coordinates): length/magnitude of a line segment.  This line segment does not have
    an origin point, or a termination point.
    ie <1, 4> signifies a vector that travels 1 unit in the x, and 4 units in the y.
    Addition:
        vector + vector = vector
            |- <u0, u1> + <v0, v1> = <u0+v0, u1+v1>

Vector / Point
    Addition:
        point + vector = point
        point - point = displacement between two points (vector)

"""

"""##  LINEAR TRANSFORMATIONS
Vector Notation
    [2, 3]
    [1, 4]
    
Matrix Notation
    [11, 12, 13, 14]
    [21, 22, 23, 24]
    [31, 32, 33, 34]
    [41, 42, 43, 44]
    
Multiplication????
    [2, 3] [5] == [5*2 + 1*3] == [13]
    [1, 4] [1] == [5*1 + 1*4] == [9]    ==> <13, 9>
        

"""