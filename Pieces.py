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

    def positions(self, x, y , moves, distance):
        tPositions = []
        if "Cardinal" in moves:
            tPositions.append((x+distance, y))
            tPositions.append((x-distance, y))
            tPositions.append((x, y+distance))
            tPositions.append((x, y-distance))
        if "Diagonal" in moves:
            tPositions.append((x+distance, y+distance))
            tPositions.append((x-distance, y+distance))
            tPositions.append((x+distance, y-distance))
            tPositions.append((x-distance, y-distance))
        if "Horse" == moves:
            tPositions = ((x-1, y-2), (x+1, y-2), (x-2, y-1), (x+2, y-1),
                          (x-1, y+2), (x+1, y+2), (x-2, y+1), (x+2, y+1))
        if "Pawn" == moves:
            m = -1 if self.v == 0 else 1
            tPositions.append((x, y+m))
            if not self.moved:
                tPositions.append((x, y+2*m))
            
        positions = []
        for pos in tPositions:
            if min(pos) < 0 or max(pos) > 7:
                positions.append(None)
            else:
                positions.append(pos)
        return positions

    def path(self, x = None, y = None, allyPieces = None, enemyPieces = None, moves = None):
        moveset = []
        for j in range(8):
            line = []
            for i in range(8):
               line.append(False)
            moveset.append(line)

        if moves == None:
            return moveset

        elif moves == "Horse" or moves == "Pawn":
            m = -1 if self.v == 0 else 1
            distance = 5
        else:
            distance = 1

        locked = [False, False, False, False, False, False, False, False]
        pieces = enemyPieces + allyPieces
        enemySize = len(enemyPieces)
        while(distance < 6):
            possibles = self.positions(x, y , moves, distance)
            for l, pos in enumerate(possibles):
                if pos == None or locked[l]:
                    continue
                flag = True

                for i, piece in enumerate(pieces):
                    x2, y2 = utils.coordToBoard(piece.x, piece.y)

                    if x2 == pos[0] and pos[1] == y2 and flag :
                        if i < enemySize and moves != "Pawn":
                            moveset[pos[1]][pos[0]] = piece
                        flag = False
                        locked[l] = True
                        break
                    # Pawn moves
                    elif moves == "Pawn" and  i < enemySize:
                        if y2 == y+m and (x2 == x+1 or x2 == x-1):
                            moveset[y2][x2] = piece
                        # Passant
                        if (isinstance(piece, Pawn) and piece.justMoved and
                             y2 == y and (x2 == x+1 or x2 == x-1)):
                            moveset[y+m][x2] = ((x2, y+m), piece) 
                    
                if flag:
                    moveset[pos[1]][pos[0]] = True

            if "Single" in moves:
                break

            distance += 1
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
        return super().path(x, y, allyPieces, enemyPieces, "Pawn")

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
        return super().path(x, y, allyPieces, enemyPieces, "Horse")

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
