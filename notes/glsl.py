## DATA TYPES
"""
    bool
    int
    float
    vec2/3/4
        array access
            vec4 = (1, 2, 3, 4)
            x == vec4.x == vec4[0]
    mat2/3/4
"""


## MAIN FUNCTION
"""
* Shaders must contain main functions
    This is written in a c-style syntax

void main()
{
    // comment
}
"""


## VERTEX BUFFERS
"""
#### buffers
glGenBuffers(count)
    where do these arbitrary buffers come from?  Just makes a new one?
    is this just instantiating a new buffer on the GPU?
glBindBuffer(bind_target, buffer)
glBufferData(bind_target, buffer_data, buffer_usage)

#### attributes
glGetAttribLocation (program_ref, variable_name): Returns an AttributeReference named <variable_name>
    program_ref (program): program that has the attribute variable
    variable_name(string?)
    returns AttributeReference
glVertexAttribPointer (variable_ref, size, base_type, normalize, stride, offset)
    variable_ref (AttributeReference): to receive data from the Vertex Buffer 
        This should be instantiated with the glGetAttribLocation call
glEnableVertexAttrib(variable_ref): enables the attribute

"""

"""
Overview

Passing data between stages of the pipeline
* Uses TYPE MODIFIERS
    type modifiers are essentially hard coded keyword args which are used to pass arbitrary
    data between steps in the Graphics Pipeline

    in (vertex): values supplied from a BUFFER
    in (fragment): values supplied from VERTEX SHADER

    out (vertex): values supplied to FRAGMENT SHADER
    out (fragment): values stored in color buffer (color, depth, stencil)
    outputs MUST define specific outputs for VERTEX/FRAGMENT shaders
        Vertex
            gl_Position = vec4(0.0, 0.0, 0.0, 1.0)
        Fragment
            gl_FragColor = vec4(0.5, 0.5, 0.5, 1.0)
            gl_Depth = ?

"""

## SNIPPETS
## ## 01
"""
void main()
{
  foo; // constant expressions are dynamically uniform.
  
  uint value = 21; // 'value' is dynamically uniform.
  value = range.x; // still dynamically uniform.
  value = range.y + fromRange.y; // not dynamically uniform; current contents come from a non-dynamically uniform source.
  value = 4; // dynamically uniform again.
  if (fromPrevious.y < 3.14)
    value = 12;
  value; // NOT dynamically uniform. Current contents depend on 'fromPrevious', an input variable.

  float number = abs(pairs.x); // 'number' is dynamically uniform.
  number = sin(pairs.y); // still dynamically uniform.
  number = cos(fromPrevious.x); // not dynamically uniform.

  vec4 colors = texture(tex, pairs.xy); // dynamically uniform, even though it comes from a texture.
                                        // It uses the same texture coordinate, thus getting the same texel every time.
  colors = texture(tex, fromPrevious.xy); // not dynamically uniform.

  for(int i = range.x; i < range.y; ++i)
  {
       // loop initialized with, compared against, and incremented by dynamically uniform expressions.
    i; // Therefore, 'i' is dynamically uniform, even though it changes.
  }

  for(int i = fromRange.x; i < fromRange.y; ++i)
  {
    i; // 'i' is not dynamically uniform; 'fromRange' is not dynamically uniform.
  }
}
"""

## ## FUNCTIONS
"""
void MyFunction(in float inputValue, out int outputValue, inout float inAndOutValue)
{
  inputValue = 0.0;
  outputValue = int(inAndOutValue + inputValue);
  inAndOutValue = 3.0;
}

void main()
{
  float in1 = 10.5;
  int out1 = 5;
  float out2 = 10.0;
  MyFunction(in1, out1, out2);
}
"""

