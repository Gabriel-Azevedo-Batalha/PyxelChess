import pyxel
import utils

"""
Pieces Paths needs refactoration!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

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

    def path(self, x = None, y = None, allyPieces = None, enemyPieces = None, moves = None):
        moveset = []
        for j in range(8):
            line = []
            for i in range(8):
               line.append(False)
            moveset.append(line)

        if moves == None:
            return moveset
        else:
            d = y
            u = y
            l = x
            r = x
            flags = [False, False, False, False, False, False, False, False]
            while(d < 7 or u > 0 or l > 0 or r < 7):
                d += 1
                u -= 1
                l -= 1
                r += 1

                for piece in enemyPieces:
                    x2, y2 = utils.coordToBoard(piece.x, piece.y)
                    if "Diagonal" in moves:
                        if x2 == r and d == y2 and not flags[0]:
                            moveset[d][r] = piece
                            flags[0] = True
                        if x2 == l and d == y2 and not flags[1]:
                            moveset[d][l] = piece
                            flags[1] = True
                        if x2 == r and u == y2 and not flags[2]:
                            moveset[u][r] = piece
                            flags[2] = True
                        if x2 == l and u == y2 and not flags[3]:
                            moveset[u][l] = piece
                            flags[3] = True
                    if "Cardinal" in moves:
                        if x2 == x and d == y2 and not flags[4]:
                            moveset[d][x] = piece
                            flags[4] = True
                        if x2 == x and u == y2 and not flags[5]:
                            moveset[u][x] = piece
                            flags[5] = True
                        if x2 == r and y == y2 and not flags[6]:
                            moveset[y][r] = piece
                            flags[6] = True
                        if x2 == l and y == y2 and not flags[7]:
                            moveset[y][l] = piece
                            flags[7] = True
                for piece in allyPieces:
                    x2, y2 = utils.coordToBoard(piece.x, piece.y)
                    if "Diagonal" in moves:
                        if x2 == r and d == y2 and not flags[0]:
                            flags[0] = True
                        if x2 == l and d == y2 and not flags[1]:
                            flags[1] = True
                        if x2 == r and u == y2 and not flags[2]:
                            flags[2] = True
                        if x2 == l and u == y2 and not flags[3]:
                            flags[3] = True
                    if "Cardinal" in moves:
                        if x2 == x and d == y2 and not flags[4]:
                            flags[4] = True
                        if x2 == x and u == y2 and not flags[5]:
                            flags[5] = True
                        if x2 == r and y == y2 and not flags[6]:
                            flags[6] = True
                        if x2 == l and y == y2 and not flags[7]:
                            flags[7] = True
                if "Diagonal" in moves:
                    if d < 8 and r < 8 and not flags[0]:
                        moveset[d][r] = True
                    if d < 8 and l >= 0 and not flags[1]:
                        moveset[d][l] = True
                    if u >= 0 and r < 8 and not flags[2]:
                        moveset[u][r] = True
                    if u >= 0 and l >= 0 and not flags[3]:
                        moveset[u][l] = True
                if "Cardinal" in moves:
                    if d < 8 and not flags[4]:
                        moveset[d][x] = True
                    if u >= 0 and not flags[5]:
                        moveset[u][x] = True
                    if r < 8 and not flags[6]:
                        moveset[y][r] = True
                    if l >= 0 and not flags[7]:
                        moveset[y][l] = True
                if not False in flags or "Single" in moves:
                    break
        return moveset

    def moves(self, moveset):
        moves = []
        for row in moveset:
            for column in row:
                if column != False:
                    moves.append(column)
        return moves

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
        moveset = super().path()
         # Init
        m = -1 if self.v == 0 else 1
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
            # Passant
            if (isinstance(piece, Pawn) and 
            piece.justMoved and y2 == y and (x2 == x+1 or x2 == x-1)):
                moveset[y+m][x2] = ((x2, y+m), piece) 
        # Ally Collision
        for piece in allyPieces:
            x2, y2 = utils.coordToBoard(piece.x, piece.y)
            # Block first move
            if y2 == y+2*m and x2 == x:
                moveset[y2][x] = False
            # Block Move
            if y2 == y+m and x2 == x:
                moveset[y2][x2] = False
                if not self.moved:
                    moveset[y2+m][x] = False
        return moveset

    def draw(self):
        super().draw()

class Rook(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.u = 12

    def draw(self):
        super().draw()

    def path(self, x, y, allyPieces, enemyPieces):
        return super().path(x, y, allyPieces, enemyPieces, ["Cardinal"])

class Horse(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.u = 24

    def draw(self):
        super().draw()

    def path(self, x, y, allyPieces, enemyPieces):
        moveset = super().path()

        if y > 0:
            if y > 1:
                if x > 0:
                    moveset[y-2][x-1] = True
                if x < 7:
                    moveset[y-2][x+1] = True
            if x > 1:
                moveset[y-1][x-2] = True
            if x < 6:
                 moveset[y-1][x+2] = True
        if y < 7:
            if y < 6:
                if x > 0:
                    moveset[y+2][x-1] = True
                if x < 7:
                    moveset[y+2][x+1] = True
            if x > 1:
                moveset[y+1][x-2] = True
            if x < 6:
                 moveset[y+1][x+2] = True

        for piece in enemyPieces:
            x2, y2 = utils.coordToBoard(piece.x, piece.y)
            # Up
            if y2 == y-2:
                # Left
                if x2 == x-1:
                    moveset[y-2][x-1] = piece
                # Right
                if x2 == x+1:
                     moveset[y-2][x+1] = piece
            # Down 
            if y2 == y+2:
                # Left
                if x2 == x-1:
                    moveset[y+2][x-1] = piece
                #  Right
                if x2 == x+1:
                     moveset[y+2][x+1] = piece
            # Left 
            if x2 == x-2:
                # Up
                if y2 == y-1:
                    moveset[y-1][x-2] = piece
                # Down
                if y2 == y+1:
                    moveset[y+1][x-2] = piece
            # Right 
            if x2 == x+2:
                # Up
                if y2 == y-1:
                    moveset[y-1][x+2] = piece
                # Down
                if y2 == y+1:
                    moveset[y+1][x+2] = piece

        for piece in allyPieces:
            x2, y2 = utils.coordToBoard(piece.x, piece.y)
            # Up
            if y2 == y-2:
                # Left
                if x2 == x-1:
                    moveset[y-2][x-1] = False
                # Right
                if x2 == x+1:
                     moveset[y-2][x+1] = False
            # Down 
            if y2 == y+2:
                # Left
                if x2 == x-1:
                    moveset[y+2][x-1] = False
                #  Right
                if x2 == x+1:
                     moveset[y+2][x+1] = False
            # Left 
            if x2 == x-2:
                # Up
                if y2 == y-1:
                    moveset[y-1][x-2] = False
                # Down
                if y2 == y+1:
                    moveset[y+1][x-2] = False
            # Right 
            if x2 == x+2:
                # Up
                if y2 == y-1:
                    moveset[y-1][x+2] = False
                # Down
                if y2 == y+1:
                    moveset[y+1][x+2] = False

        return moveset

class Bishop(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.u = 36
    def draw(self):
        super().draw()
    
    def path(self, x, y, allyPieces, enemyPieces):
       return super().path(x, y, allyPieces, enemyPieces, ["Diagonal"])

    
class King(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.u = 48

    def draw(self):
        super().draw()

    def path(self, x, y, allyPieces, enemyPieces):
        return super().path(x, y, allyPieces, enemyPieces, ["Cardinal", "Diagonal", "Single"])

class Queen(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.u = 60

    def draw(self):
        super().draw()

    def path(self, x, y, allyPieces, enemyPieces):
        return super().path(x, y, allyPieces, enemyPieces, ["Cardinal", "Diagonal"])
