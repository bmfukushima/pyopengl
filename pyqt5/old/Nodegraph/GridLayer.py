from OpenGL import GL


class GridLayer(object):
    """'
Object that defines all of the Grid Layer drawing.

This will hold all of the properties/utils/etc for everything
that is involved in drawing the Grid.

Args:
    **  gridOpacity (bool): Determines whether or not the grid lines will be
            dimmed based off of their distance to the camera.
    **  gridSpacing (int): The amount of units between the coordinates on
            the grid
    ** gridDisplayType (int): How to display the grid to the user
            0 - default grid lines
            1 - display as cross (+) at intersection
            2 - display as point at intersection
            3 - Square?
            4 - Triangle?
    """
    def __init__(
        self,
        gridOpacity=True,
        gridSpacing=5,
        gridColor=(1, 1, 1),
        gridDisplayType=2,
        gridIntersectionSize=0.5
    ):
        super(GridLayer, self).__init__()
        self.setGridOpacity(gridOpacity)
        self.setGridSpacing(gridSpacing)
        self.setGridColor(*gridColor)
        self.setGridDisplayType(gridDisplayType)
        self.grid_intersection_size = gridIntersectionSize

    def getAttributes(self):
        """
        Gets all of the necessary attributes for computing the grid lines

        Returns:
            num_columns (int)
            num_rows (int)
            pan_x (float)
            pan_y (float)
            x_offset (float)
            y_offset (float)
            spacing (int)
        """
        spacing = self.getGridSpacing()
        pan_x = self.pan_pos.x()
        pan_y = self.pan_pos.y()

        num_columns = int((self.zoom_factor / spacing) * self.aspect_ratio) + 2
        num_rows = int((self.zoom_factor / spacing)) + 2

        # get camera offset (returns pan pos to integer)
        x_offset = pan_x % spacing
        y_offset = pan_y % spacing

        return num_columns, num_rows, pan_x, pan_y, x_offset, y_offset, spacing

    def drawGrid(self):
        """
        draws the background grid
        """

        # get attrs
        self.__setupGridLineOpacity()

        # setup GL
        GL.glPolygonMode(GL.GL_FRONT, GL.GL_LINE)
        GL.glLineWidth(1)
        GL.glColor4f(1, 1, 1, 1)

        # enable opacity
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        # draw grid
        display_type = self.getGridDisplayType()
        if display_type == 0:
            self.drawLines(*self.getAttributes())
        else:
            self.drawIntersection(*self.getAttributes(), display_type)

    def drawIntersection(
            self,
            num_columns,
            num_rows,
            pan_x,
            pan_y,
            x_offset,
            y_offset,
            spacing,
            display_type
        ):
        """
        Draws the grid as primitives at intersections
        """

        # get x positions
        xpos_list = []
        for line in range(-num_columns, num_columns):
            line *= spacing
            xunit = {}
            xunit['xpos'] = (line + x_offset) / self.aspect_ratio
            xunit['grid_number'] = pan_x - x_offset - line
            xpos_list.append(xunit)
        size = self.grid_intersection_size
        #print(size)
        # draw intersections
        if display_type == 1:
            GL.glBegin(GL.GL_LINES)
        elif display_type == 2:
            GL.glPointSize(2)
            GL.glBegin(GL.GL_POINTS)

        for line in range(-num_rows, num_rows):
            line *= spacing
            y_grid_number = pan_y + line - y_offset
            y = line - y_offset
            for xunit in xpos_list:
                x = xunit['xpos']
                x_grid_number = xunit['grid_number']
                '''
                if x_grid_number % 25 == 0 and y_grid_number % 25 == 0:
                    size *= 5
                '''
                max_size = max(self.width(), self.height()) * 0.5
                screen_size = (size / self.zoom_factor) * max_size
                #print(self.width(), self.height(), screen_size)
                if size > .05:
                    if display_type == 1:
                        self.drawPlus(x, y)
                    elif display_type == 2:
                        self.drawPoint(x, y)

        GL.glEnd()

    def drawLines(
        self,
        num_columns,
        num_rows,
        pan_x,
        pan_y,
        x_offset,
        y_offset,
        spacing
    ):
        """
        Draws the grid as lines
        """

        # draw vertical lines
        for line in range(-num_columns, num_columns):
            line *= spacing
            grid_number = pan_x - x_offset - line

            self.__finalizeGridLineOpacity(grid_number)

            GL.glBegin(GL.GL_LINES)
            GL.glVertex3f(((line + x_offset) / self.aspect_ratio), num_rows * spacing, self.GRID_DEPTH)
            GL.glVertex3f(((line + x_offset) / self.aspect_ratio), -num_rows * spacing, self.GRID_DEPTH)
            GL.glEnd()
        # draw horizontal lines
        for line in range(-num_rows, num_rows):

            line *= spacing
            grid_number = pan_y + line - y_offset
            self.__finalizeGridLineOpacity(grid_number)

            GL.glBegin(GL.GL_LINES)
            GL.glVertex3f((num_columns * spacing) / self.aspect_ratio, line - y_offset, self.GRID_DEPTH)
            GL.glVertex3f((-num_columns * spacing) / self.aspect_ratio, line - y_offset, self.GRID_DEPTH)
            GL.glEnd()

    def drawPlus(self, x, y):
        size = self.grid_intersection_size
        GL.glVertex3f(x - (size / self.aspect_ratio), y, self.GRID_DEPTH)
        GL.glVertex3f(x + (size / self.aspect_ratio), y, self.GRID_DEPTH)
        GL.glVertex3f(x, y + size, self.GRID_DEPTH)
        GL.glVertex3f(x, y - size, self.GRID_DEPTH)

    def drawPoint(self, x, y):
        GL.glVertex3f(x, y, self.GRID_DEPTH)

    def drawShape(self):
        pass

    """ UTILS """
    def __setupGridLineOpacity(self):
        """
        Does the initial setup for the opacity of the grid lines.
        This will determine the base opactiy for each grid line.
        """
        if self.getGridOpacity() is True:
            divisor = int(self.zoom_factor - self.MIN_ZOOM)
            if divisor < 1:
                divisor = 1
            opacity = (1 / divisor) * 10

        else:
            opacity = 1
        self.setGridLineOpacity(opacity)

    def __finalizeGridLineOpacity(self, grid_number, multiplier=2):
        """
        Determines the finale opacity of a specified grid line.  This
        takes multiples of certain numbers, and increases the opacity
        of those multiples.

        Args:
            *   grid_number (int): the line number for the current grid
                    that is currently being worked on
            ** multiplier (float): how much each multiples opacity
                    should be increased by
        """
        opacity_list = [5, 10, 25, 50, 100, 500]
        opacity = self.getGridLineOpacity()
        if grid_number == 0.0:
            GL.glLineWidth(2)
            GL.glColor4f(*self.getGridColor(), 1)

        else:
            GL.glLineWidth(1)
            for n in opacity_list:
                if grid_number % n == 0:
                    opacity *= multiplier
            GL.glColor4f(*self.getGridColor(), opacity)

    """ PROPERTIES """
    def setGridColor(self, r, g, b):
        self._grid_color_r = r
        self._grid_color_g = g
        self._grid_color_b = b

    def getGridColor(self):
        return self._grid_color_r, self._grid_color_g, self._grid_color_b

    def getGridDisplayType(self):
        return self._grid_display_type

    def setGridDisplayType(self, grid_display_type):
        self._grid_display_type = grid_display_type

    def getGridLineOpacity(self):
        return self._grid_line_opacity

    def setGridLineOpacity(self, grid_line_opacity):
        self._grid_line_opacity = grid_line_opacity

    def getGridOpacity(self):
        return self._grid_opacity

    def setGridOpacity(self, grid_opacity):
        self._grid_opacity = grid_opacity

    def getGridSpacing(self):
        return self._grid_spacing

    def setGridSpacing(self, grid_spacing):
        self._grid_spacing = grid_spacing

    @property
    def grid_intersection_size(self):
        return self._grid_intersection_size

    @grid_intersection_size.setter
    def grid_intersection_size(self, grid_intersection_size):
        self._grid_intersection_size = grid_intersection_size
