class DisplayLines():
    def __init__(self,ssd1351):
		self.ds = ssd1351
		self.ds.clear()

    def hline(self, x, y, w, color):
        if self.ds.is_off_grid(x, y, x + w - 1, y):
           return
        line = color.to_bytes(2, 'big') * w
        self.ds.block(x, y, x + w - 1, y, line)

    def line(self, x1, y1, x2, y2, color):
        """Draw a line using Bresenham's algorithm.
        Args:
            x1, y1 (int): Starting coordinates of the line
            x2, y2 (int): Ending coordinates of the line
            color (int): RGB565 color value.
        """
        # Check for horizontal line
        if y1 == y2:
            if x1 > x2:
                x1, x2 = x2, x1
            self.ds.hline(x1, y1, x2 - x1 + 1, color)
            return
        # Check for vertical line
        if x1 == x2:
            if y1 > y2:
                y1, y2 = y2, y1
            self.ds.vline(x1, y1, y2 - y1 + 1, color)
            return
        # Confirm coordinates in boundary
        if self.ds.is_off_grid(min(x1, x2), min(y1, y2),
                            max(x1, x2), max(y1, y2)):
            return
        # Changes in x, y
        dx = x2 - x1
        dy = y2 - y1
        # Determine how steep the line is
        is_steep = abs(dy) > abs(dx)
        # Rotate line
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        # Swap start and end points if necessary
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        # Recalculate differentials
        dx = x2 - x1
        dy = y2 - y1
        # Calculate error
        error = dx >> 1
        ystep = 1 if y1 < y2 else -1
        y = y1
        for x in range(x1, x2 + 1):
            # Had to reverse HW ????
            if not is_steep:
                self.ds.draw_pixel(x, y, color)
            else:
                self.ds.draw_pixel(y, x, color)
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx

    def lines(self, coords, color):
        """Draw multiple lines.
        Args:
            coords ([[int, int],...]): Line coordinate X, Y pairs
            color (int): RGB565 color value.
        """
        # Starting point
        x1, y1 = coords[0]
        # Iterate through coordinates
        for i in range(1, len(coords)):
            x2, y2 = coords[i]
            self.line(x1, y1, x2, y2, color)
            x1, y1 = x2, y2
            
    def vline(self, x, y, h, color):
        """Draw a vertical line.
        Args:
            x (int): Starting X position.
            y (int): Starting Y position.
            h (int): Height of line.
            color (int): RGB565 color value.
        """
        # Confirm coordinates in boundary
        if self.ds.is_off_grid(x, y, x, y + h):
            return
        line = color.to_bytes(2, 'big') * h
        self.ds.block(x, y, x, y + h - 1, line) 
            
    def clear(self):
	    self.ds.clear()
	
    def cleanup(self):
	    self.ds.cleanup()
