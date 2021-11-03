import pyxel
import utils

class Piece():
    def __init__(self, x, y, white):
        if white:
           self.v = 0
        else:
            self.v = 8
        self.x = x
        self.y = y
        self.highlighted = False
        self.moved = False
        

    def draw(self):
        pyxel.load("assets.pyxres")
        color = -1 if self.highlighted else pyxel.COLOR_YELLOW
        pyxel.blt(self.x, self.y, 0, self.v, self.u, 8, 12, color)
class Pawn(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.u = 0
        self.justMoved = False

    def path(self, x, y, allyPieces, enemyPieces):
        # Init
        m = -1 if self.v == 0 else 1
        moveset = []
        for j in range(8):
            line = []
            for i in range(8):
               line.append(False)
            moveset.append(line)
        # First Move
        if not self.moved:
            moveset[y+m][x] = True
            moveset[y+2*m][x] = True
        # Default Move
        elif y+m < 8 and y+m > 0:
            moveset[y+m][x] = True
        # Enemy Collision
        for piece in enemyPieces:
            x2, y2 = utils.coordToBoard(piece.x, piece.y)
            # Block first move
            if y2 == y+2*m and x2 == x:
                moveset[y+2*m][x] = False
            if y2 == y+m:
                # Capture
                if x2 == x+1 or x2 == x-1:
                    moveset[y2][x2] = piece
                # Block Move
                if x2 == x:
                    moveset[y2][x2] = False
            # Special Move
            if (isinstance(piece, Pawn) and 
            piece.justMoved and y2 == y and (x2 == x+1 or x2 == x-1)):
                print("That's it!")
                moveset[y+m][x2] = ((x2, y+m), piece) 

        for piece in allyPieces:
            x2, y2 = utils.coordToBoard(piece.x, piece.y)
            # Block first move
            if y2 == y+2*m and x2 == x:
                moveset[y+2*m][x] = False
            # Block Move
            if y2 == y+m and x2 == x:
                moveset[y2][x2] = False
        return moveset

    def draw(self):
        super().draw()

class Rook(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.u = 12
    def draw(self):
        super().draw()

class Horse(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.u = 24
    def draw(self):
        super().draw()

class Bishop(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.u = 36
    def draw(self):
        super().draw()

class King(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.u = 48
    def draw(self):
        super().draw()

class Queen(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.u = 60
    def draw(self):
        super().draw()