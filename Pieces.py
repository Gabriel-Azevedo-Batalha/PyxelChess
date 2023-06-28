import pyxel
import utils

"""
Add passant as a check escape move
"""



class Piece():
    def __init__(self, x, y, white):
        pyxel.load("assets/assets.pyxres")
        self.v = 0 if white else 8
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

    def path(self, x, y, allyPieces, enemyPieces, moves):
        moveset = []
        for j in range(8):
            line = []
            for i in range(8):
               line.append(False)
            moveset.append(line)

        if moves == "Pawn":
            m = -1 if self.v == 0 else 1
            distance = 5
        elif moves == "Horse":
            distance = 5
        else:
            distance = 1

        locked = [False]*8
        pieces = enemyPieces + allyPieces
        enemySize = len(enemyPieces)
        while(distance <= 7):
            possibles = self.positions(x, y , moves, distance)
            for l, pos in enumerate(possibles):
                if pos == None or locked[l]:
                    continue
                flag = True

                for i, piece in enumerate(pieces):
                    x2, y2 = utils.coordToBoard(piece.x, piece.y)

                    if x2 == pos[0] and pos[1] == y2 and flag :
                        flag = False
                        locked[l] = True
                        if moves != "Pawn":
                            t = "Capture" if i < enemySize else "Defend"
                            moveset[pos[1]][pos[0]] = {"type": t, "target": piece, "pos" : (pos[0], pos[1])}
                            break
                    # Pawn Captures
                    elif moves == "Pawn" and  i < enemySize:
                        # Default
                        if y2 == y+m and (x2 == x+1 or x2 == x-1):
                            moveset[y2][x2] = {"type": "Capture", "target": piece, "pos" : (x2, y+m)}
                        # Passant
                        if (isinstance(piece, Pawn) and piece.justMoved and
                            y2 == y and (x2 == x+1 or x2 == x-1)):
                            moveset[y+m][x2] = {"type": "Passant", "target": piece, "pos" : (x2, y+m)}
                    
                if flag and not (moves == "Pawn" and locked[0]):
                    t = "PMove" if moves == "Pawn" else "Move"
                    moveset[pos[1]][pos[0]] = {"type": t, "pos" : (pos[0], pos[1])}

            if "Single" in moves:
                break

            distance += 1

        return moveset

    def moves(self, moveset, filter = []):
        moves = []
        x, y = utils.coordToBoard(self.x, self.y)
        for row in moveset:
            for column in row:
                if column != False and column["type"] not in filter:
                    moves.append(column)           
        
        if isinstance(self, Pawn) and y > 0 and y < 7 and "CMove" not in filter:
                m = -1 if self.v == 0 else 1
                if x > 0:
                    moves.append({"type": "Move", "pos": (x-1, y+m)})
                if x < 7:
                    moves.append({"type": "Move", "pos": (x+1, y+m)})

        return moves

    def draw(self):
        
        color = None if self.highlighted else pyxel.COLOR_YELLOW
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

    def forbid(self, moveset, allyPieces, enemyPieces):
        forbidden = []

        for piece in enemyPieces:
            x, y = utils.coordToBoard(piece.x, piece.y)
            toAdd = piece.moves(piece.path(x, y, enemyPieces, allyPieces), ["PMove"])
            for a in toAdd:
                    forbidden.append(a)
        for f in forbidden:
                moveset[f["pos"][1]][f["pos"][0]] = False

        return moveset

    

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
