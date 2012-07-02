import drawing
import itertools
import random

LINE_HEIGHT = 0.03
LINE_SPACING = 0.02
TOP_OF_BOARD = 0.25

class Board(object):
    def __init__(self, size=1):
        self.size = size
        #True indicates that the line has been crossed out
        self._state = [None]*size
        for i in range(size):
            self._state[i] = [False]*(i + 1)

    def is_occupied(self, row, col):
        return self._state[row][col]

    def move(self, row, col_start, col_end):
        """Makes a move on row beginning at col_start (inclusive) 
        and ending at col_end (inclusive).
        
        All indices are zero-based"""
        assert not any(self._state[row][col_start:col_end + 1]), "Illegal move"
        for i in range(col_start, col_end + 1):
            self._state[row][i] = True
    
    def is_gameover(self):
        return all(itertools.chain(*self._state))

class UI(object):
    def init(self, board):
        pass

class TerminalUI(UI):
    def __init__(self):
        super(TerminalUI, self).__init__()

    def _draw_board(self, board):
        for row in range(board.size):
            line =  '%d:' % row
            for col in range(row + 1):
                if board.is_occupied(row, col):
                    line += '+'
                else:
                    line += '|'
            print line

    def get_player_move(self, board):
        """Get player's move

        return: the updated Board object"""
        self._draw_board(board)
        inp = raw_input("Input move: [row],[col start],[lines to cross out]")
        row, col_start, lines = inp.split(',')
        board.move(int(row), int(col_start), int(col_start) + int(lines) - 1)
        return board
    
    def ai_move(self, move, board):
        self._draw_board(board)
        num_lines = move[2] - move[1] + 1
        print "AI crossed out {num} line{plural} on row {row} starting at column {col}".format(
                row=move[0], col=move[1], num=num_lines, plural='s' if num_lines > 1 else '') 

class PhysicalUI(UI):
    def __init__(self):
        super(PhysicalUI, self).__init__()
        self.drawing = drawing.Drawing()

    def init(self, board):
        """Draw the board"""
        for row in range(board.size):
            row_width = LINE_SPACING * row
            for line in range(row + 1):
                x = line * LINE_SPACING - row_width / 2.0
                y = TOP_OF_BOARD - row * LINE_HEIGHT * 1.5
                self.drawing.line(x, y, x, y - LINE_HEIGHT)

class Strategy(object):
    def select_move(self, board):
        pass

class RandomStrategy(Strategy):
    def select_move(self, board):
        while True:
            row = random.randint(0, board.size - 1)
            col = random.randint(0, row)
            if not board.is_occupied(row, col):
                return (row, col, col)

class GameController(object):
    def __init__(self):
        self.board = Board(3)
        self.strategy = RandomStrategy()
        self.ui = TerminalUI()

    def run(self):
        while True:
            self.board = self.ui.get_player_move(self.board)
            if self.board.is_gameover():
                print "You win"
                break
            ai_move = self.strategy.select_move(self.board)
            self.ui.ai_move(ai_move, self.board)
            self.board.move(*ai_move)
            if self.board.is_gameover():
                print "You lose"
                break

if __name__ == "__main__":
    controller = GameController()
    controller.run()









