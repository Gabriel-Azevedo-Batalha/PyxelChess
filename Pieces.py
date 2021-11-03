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

    def path(self):
        moveset = []
        for j in range(8):
            line = []
            for i in range(8):
               line.append(False)
            moveset.append(line)
        return moveset

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
        moveset = super().path()
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
                print("That's it!")
                moveset[y+m][x2] = ((x2, y+m), piece) 
        # Ally Collision
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
    def path(self, x, y, allyPieces, enemyPieces):
        moveset = super().path()

        d = y
        u = y
        l = x
        r = x
        while(d < 7 or u > 0 or l > 0 or r < 7):
            d += 1
            u -= 1
            l -= 1
            r += 1
            for piece in enemyPieces:
                x2, y2 = utils.coordToBoard(piece.x, piece.y)
                if x2 == x and d == y2:
                    moveset[d][x] = piece
                    d = 8
                if x2 == x and u == y2:
                    moveset[u][x] = piece
                    u = -1
                if x2 == l and y == y2:
                    moveset[y][l] = piece
                    l = -1
                if x2 == r and y == y2:
                    moveset[y][r] = piece
                    r = 8
            for piece in allyPieces:
                x2, y2 = utils.coordToBoard(piece.x, piece.y)
                if x2 == x and d == y2:
                    d = 8
                if x2 == x and u == y2:
                    u = -1
                if x2 == l and y == y2:
                    l = -1
                if x2 == r and y == y2:
                    r = 8
            if d < 8:
                moveset[d][x] = True
            if u >= 0:
                moveset[u][x] = True
            if r < 8:
                moveset[y][r] = True
            if l >= 0:
                moveset[y][l] = True
       
        return moveset

class Horse(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.u = 24

    def draw(self):
        super().draw()

    def path(self, x, y, allyPieces, enemyPieces):
        moveset = super().path()



        return moveset

class Bishop(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.u = 36
    def draw(self):
        super().draw()

    def path(self, x, y, allyPieces, enemyPieces):
        moveset = super().path()

        d = y
        u = y
        l = x
        r = x
        flags = [False, False, False, False]
        while(d < 7 or u > 0 or l > 0 or r < 7):
            d += 1
            u -= 1
            l -= 1
            r += 1
            for piece in enemyPieces:
                x2, y2 = utils.coordToBoard(piece.x, piece.y)
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
            for piece in allyPieces:
                x2, y2 = utils.coordToBoard(piece.x, piece.y)
                if x2 == r and d == y2 and not flags[0]:
                    flags[0] = True
                if x2 == l and d == y2 and not flags[1]:
                    flags[1] = True
                if x2 == r and u == y2 and not flags[2]:
                    flags[2] = True
                if x2 == l and u == y2 and not flags[3]:
                    flags[3] = True
            if d < 8 and r < 8 and not flags[0]:
                moveset[d][r] = True
            if d < 8 and l >= 0 and not flags[1]:
                moveset[d][l] = True
            if u >= 0 and r < 8 and not flags[2]:
                moveset[u][r] = True
            if u >= 0 and l >= 0 and not flags[3]:
                moveset[u][l] = True
            if not False in flags:
                break
       
        return moveset

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