
class DisplayText():
    def __init__(self,ssd1351):
		self.ds = ssd1351
		self.ds.clear()
	
    def letter(self,x, y, letter, font, color, background=0,
                    landscape=False):
        """Draw a letter.
        Args:
            x (int): Starting X position.
            y (int): Starting Y position.
            letter (string): Letter to draw.
            font (XglcdFont object): Font.
            color (int): RGB565 color value.
            background (int): RGB565 background color (default: black).
            landscape (bool): Orientation (default: False = portrait)
        """
        buf, w, h = font.get_letter(letter, color, background,
                                    landscape)
        # Check for errors
        if w == 0:
            return w, h

        if landscape:
            y -= w
            if self.ds.is_off_grid(x, y, x + h - 1, y + w - 1):
                return
            self.ds.block(x, y,
                       x + h - 1, y + w - 1,
                       buf)
        else:
            if self.ds.is_off_grid(x, y, x + w - 1, y + h - 1):
                return
            self.ds.write_cmd(self.ds.SET_REMAP, 0x75)  # Vertical address increment
            self.ds.block(x, y,
                       x + w - 1, y + h - 1,
                       buf)
            self.ds.write_cmd(self.ds.SET_REMAP, 0x74)  # Switch back to horizontal
        return w, h

    def text(self, x, y, text, font, color,  background=0,landscape=False, spacing=1):
        """Draw text.
        Args:
            x (int): Starting X position.
            y (int): Starting Y position.
            text (string): Text to draw.
            font (XglcdFont object): Font.
            color (int): RGB565 color value.
            background (int): RGB565 background color (default: black).
            landscape (bool): Orientation (default: False = portrait)
            spacing (int): Pixels between letters (default: 1)
        """
        for letter in text:
            # Get letter array and letter dimensions
            w, h = self.letter(x, y, letter, font, color, background,landscape)
            # Stop on error
            if w == 0 or h == 0:
                print('Invalid width {0} or height {1}'.format(w, h))
                return

            if landscape:
                # Fill in spacing
                if spacing:
                    self.ds.fill_hrect(x, y - w - spacing, h, spacing, background)
                # Position y for next letter
                y -= (w + spacing)
            else:
                # Fill in spacing
                if spacing:
                    self.ds.fill_vrect(x + w, y, spacing, h, background)
                # Position x for next letter
                x += w + spacing

    def clear(self):
		self.ds.clear()
	
    def cleanup(self):
		self.ds.cleanup()
