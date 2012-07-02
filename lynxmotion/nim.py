import drawing

LINE_HEIGHT = 0.03
LINE_SPACING = 0.02
TOP_OF_BOARD = 0.25

class Board(object):
    def __init__(self, size=1):
        self.drawing = drawing.Drawing()
        self.size = size

    def init(self):
        """Draw the board"""
        for row in range(self.size):
            row_width = LINE_SPACING * row
            for line in range(row + 1):
                x = line * LINE_SPACING - row_width / 2.0
                y = TOP_OF_BOARD - row * LINE_HEIGHT * 1.5
                self.drawing.line(x, y, x, y - LINE_HEIGHT)


