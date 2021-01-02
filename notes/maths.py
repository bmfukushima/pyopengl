
#       VECTORS
"""
## VOCAB
CAPITAL BOLD = MATRIX
LOWER BOLD = VECTOR

Affine Transformation (): translate/rotate/scale

Basis Vectors (vector): using the vectors i=<1,0> and j=<0,1>,
    any vector can be written in terms of these vectors using
    VECTOR ADDITION and SCALAR MULTIPLICATION.
        |- v = <x,y>
            ==> <x,0> + <0,y>
            ==> x * <1,0> + y * <0,1>
            ==> x*i + y*j

    This is one set of BASIS VECTORS, known as the STANDARD BASIS

Clip Space (coordinate system): the -1, 1 space that OpenGL draws to

Dot Product (function): Given 2 matrixes to multiply, this returns a third matrix, consisting of
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
Matrix:
    Global vs Local Transformation:
        < Local applies local (object/model matrix)first >
        Global: global matrix * model matrix
        Local: model matrix * local matrix
    Model Matrix (matrix): of local coordinates to an object.
        An object consists of its origin plus all of the transformations that are applied to it.
        The model Matrix is the resulting matrix after all transformations have been applied.

View Matrix (matrix): inverse of camera matrix
    Used to rotate world around camera, vs rotating camera around the world

Points (coordinates): position in space

Scalar (number): singular number
    Multiplication:
        scalar * vector = vector
            |- <s*v1, s*v2>
            |- 2 * <2,3> = <4,6>
            |- direction reversed when scalar is negative
                    positive --> top right
                    negative --> bot left

Transpose (process): switching between row/column and column/row in matrixes

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

##  LINEAR TRANSFORMATIONS
"""
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

##      SCALING TRANSFORMATIONS
"""
Multiplies each component of a vector by a constant
    4x4 matrix = 0, 5, 10
[x]   [r * x]   [r 0]   [x]
[y] = [s * y] = [0 s] * [y]

[x]   [r * x]   [r 0 0]   [x]
[y]   [s * y]   [0 s 0]   [y]
[z] = [t * z] = [0 0 t] * [z]
"""

##      ROTATION TRANSFORMATIONS
"""
Rotates vectors by a constant angle around the origin

    2D
[cos(x) -sin(x)]
[sin(x)  cos(x)]

    z-Axis              x-axis              y-axis
[cos(x) -sin(x) 0]  [1   0       0   ]  [ cos(x) 0 sin(x)]
[sin(x)  cos(x) 0]  [0 cos(x) -sin(0)]  [   0    1   0   ]
[  0       0    1]  [0 sin(x)  cos(x)]  [-sin(x) 0 cos(x)]

    Note:
        * since y-axis is going up down, the orientation changes,
            this is why the -sin/sin combo is flipped.
    Question:
        * how to rotate from arbitrary matrix in multiple dimensions?
                Matrix multiplication?

"""

##      TRANSLATION TRANSFORMATIONS
"""
* Start with identity matrix
* Embeds the current translation in a matrix of one higher dimensions

    1D                      2D                      3D
[1 m] [x]    [x+m]      [1 0 m] [x]   [x+m]     [1 0 0 m] [x]   [x+m]
[0 1] [1] =  [ 1 ]      [0 1 n] [y]   [y+n]     [0 1 0 n] [y]   [y+n]
                        [0 0 1] [1] = [ 1 ]     [0 0 1 p] [z]   [z+p]
                                                [0 0 0 1] [1] = [ 1 ]

* perspective division (non-linear) done after vertex shader stage
        x, y, z, w --> (x/w, y/w, z/w)
"""


##      FRUSTUM
"""
Angle of view (angle): angle between top plane/bottom plane
    Larger angle of view = larger frustum

Aspect Ratio (ratio): width of near plane / height of near plane
Far Plane (distance)
Near Plane (distance)

"""

