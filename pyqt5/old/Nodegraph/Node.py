"""DCC node object --> interface --> Node"""
"""DCC port object --> interface --> Port"""
"""DCC parameter object --> interface --> Parameter"""


class Parameter(object):
    """
    children
    name
    parent
    type
    """
    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, children):
        self._children = children

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type


class Port(object):
    """
Attributes:
    connected_ports (list): of ports that this port is connected to
    name (str):
    node (Node): node that the port is connected to
    type (bool): input port if 0 else 1
        0: input
        1: output
    """

    size = 2
    spacing = .5

    """ PROPERTIES """
    @property
    def connected_ports(self):
        return self._connected_ports

    @connected_ports.setter
    def connected_ports(self, connected_ports):
        self._connected_ports = connected_ports

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, node):
        self._node = node

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type


class Node(object):
    """
A singular node in the Nodegraphs metadata.

This has all of the data required to recreate a node in the Nodegraph.
In order to get/populate these fields, they will call the NodeInterface,
which is a an interface class that will need to be customized per DCC.

Attributes:
    color (rgb): display color of the node
    children (list): list of nodes children
    display_state(int): determines how much information will be
        display to the user.
            0: minimal, I/O
            1: enabled ports / params
            2: All ports / params
            3: User defined?
    is_edited (bool): parameter flag
    is_selected (bool)
    is_viewed (bool): resolve flag
    input_ports (list):
    name (str): Nodes name
    output_ports (list):
    parameters (Parameter): A list of parameters?
    parent (node): parent node, if none, this will be the root node
    pos (QPoint): Nodes position in world space units
    type (str): The node type
    """
    width = 10
    height = 20
    depth = 3

    def __init__(self):
        self.input_ports = []
        self.output_ports = []
        self.parameters = []

    """ PROPERTIES """
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, children):
        self._children = children

    @property
    def display_state(self):
        return self._display_state

    @display_state.setter
    def display_state(self, display_state):
        self._display_state = display_state

    @property
    def is_viewed(self):
        return self._is_viewed

    @is_viewed.setter
    def is_viewed(self, is_viewed):
        self._is_viewed = is_viewed

    @property
    def is_edited(self):
        return self._is_edited

    @is_edited.setter
    def is_edited(self, is_edited):
        self._is_edited = is_edited

    @property
    def is_selected(self):
        return self._is_selected

    @is_selected.setter
    def is_selected(self, is_selected):
        self._is_selected = is_selected

    @property
    def input_ports(self):
        return self._input_ports

    @input_ports.setter
    def input_ports(self, input_ports):
        self._input_ports = input_ports

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def output_ports(self):
        return self._output_ports

    @output_ports.setter
    def output_ports(self, output_ports):
        self._output_ports = output_ports

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        self._parameters = parameters

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._pos = pos

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

