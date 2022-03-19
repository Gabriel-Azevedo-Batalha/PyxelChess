import pyxel
from copy import deepcopy

import Pieces
import utils
from constants import OFFSET, TILESIZE

class Chess():
    def __init__(self):
        self.whites = []
        self.blacks = []
        self.capWhites = []
        self.capBlacks = []
        self.LAYOUT = (Pieces.Rook, Pieces.Horse, Pieces.Bishop, 
                    Pieces.Queen, Pieces.King, Pieces.Bishop,
                    Pieces.Horse, Pieces.Rook)

        for i in range(8):
            self.whites.append(Pieces.Pawn(*utils.boardToCoord(i, 6), True))
            self.whites.append(self.LAYOUT[i](*utils.boardToCoord(i, 7), True))
            self.blacks.append(Pieces.Pawn(*utils.boardToCoord(i, 1), False))
            self.blacks.append(self.LAYOUT[i](*utils.boardToCoord(i, 0), False))
        self.turnW = True
        self.moveset = None
        self.unit = None
        self.promoted = None
        self.passantU = None
        self.state = "Chess"
        self.check = False
        self.poss = None

        # Macros
        self.turnPieces = lambda inv: self.whites if (self.turnW and not inv) or (not self.turnW and inv) else self.blacks

    def checkCheck(self, enemyPieces, allyPieces):
        check = False
        for piece in enemyPieces:
            x, y = utils.coordToBoard(piece.x, piece.y)
            toAdd = piece.moves(piece.path(x, y, enemyPieces, allyPieces), ["Defend", "Move", "CMove", "PMove"])
            for a in toAdd:
                if isinstance(a["target"], Pieces.King):
                    check = True
        return check

    def castling(self, king, moveset, allyPieces, enemyPieces):
            def rookLogic(rook, const):
                flag = False
                backupX, backupY = king.x, king.y
                for i in range(2):
                    king.x += const*TILESIZE
                    flag = self.checkCheck(enemyPieces, allyPieces)
                    if flag:
                        break
                king.x, king.y = backupX, backupY
                if not flag:
                    x, y = utils.coordToBoard(king.x, king.y)
                    moveset[y][x+2*const] = {"type": "Castling", "Rook": rook, "RookTarget" : (x+const, y),
                                        "King": king, "KingTarget" : (x+2*const, y)}
            if not king.moved:
                lRook, rRook = None, None
                lFlag, rFlag = True, True
                for piece in allyPieces:
                    x, y = utils.coordToBoard(piece.x, piece.y)
                    _, ky = utils.coordToBoard(king.x, king.y)
                    if y == ky and x in (1, 2, 3):
                        lFlag = False
                    elif y == ky and x in (5, 6):
                        rFlag = False
                    if isinstance(piece, Pieces.Rook) and not piece.moved:
                        if piece.x < king.x and lFlag:
                            lRook = piece
                        elif rFlag:
                            rRook = piece
                    if rRook != None and not rFlag:
                        rRook = None
                    elif lRook != None and not lFlag:
                        lRook = None
                if lRook != None:
                    rookLogic(lRook, -1)
                if rRook != None:
                    rookLogic(rRook, 1)
            return moveset

    def checkCheckmate(self):
        ally = deepcopy(self.whites) if self.turnW else deepcopy(self.blacks)
        enemy = deepcopy(self.whites) if not self.turnW else deepcopy(self.blacks)
        self.poss = {}
        for piece in ally:
            possibles = []
            x2, y2 = utils.coordToBoard(piece.x, piece.y)
            toAdd = piece.moves(piece.path(x2, y2, ally, enemy), ["Defend", "CMove"])
            for a in toAdd:
                possibles.append(a)
            for p in possibles:
                xi, yi = utils.coordToBoard(piece.x, piece.y)
                piece.x, piece.y = utils.boardToCoord(*p["pos"])
                if p["type"] == "Capture":
                    t = enemy.index(p["target"])
                    tEnemy = enemy[:t] + enemy[t+1:]
                    flag = self.checkCheck(tEnemy, ally)
                else:
                    flag = self.checkCheck(enemy, ally)
                if not flag:
                    pieceToAdd = self.whites[ally.index(piece)] if self.turnW else self.blacks[ally.index(piece)]
                    if self.poss.get(pieceToAdd) == None:
                        self.poss[pieceToAdd] = [p]
                    else:
                        self.poss[pieceToAdd].append(p)

                piece.x, piece.y = utils.boardToCoord(xi, yi)

        if not len(self.poss) > 0:
            self.state = "Checkmate"

    def validateMoves(self, moves):
        if isinstance(self.unit, Pieces.King):
            out = self.castling(self.unit, self.unit.forbid(moves, self.turnPieces(False), self.turnPieces(True)), self.turnPieces(False), self.turnPieces(True))
        else:
            out = []
            for row in moves:
                toAdd = []
                for m in row:
                    if not m:
                        toAdd.append(False)
                        continue
                    enemy = self.turnPieces(True)
                    backup = self.unit.x, self.unit.y
                    self.unit.x, self.unit.y = utils.boardToCoord(*m["pos"])
                    if m["type"] == "Capture":
                        t = enemy.index(m["target"])
                        tEnemy = enemy[:t] + enemy[t+1:]
                        flag = self.checkCheck(tEnemy, self.turnPieces(False))
                    else:
                        flag = self.checkCheck(enemy, self.turnPieces(False))
                    self.unit.x, self.unit.y = backup
                    if flag:
                        toAdd.append(False)
                    else:
                        toAdd.append(m)
                out.append(toAdd)
        if self.unit.moves(out, ["CMove", "Defend"]) == []:
            self.unselectUnit()
        return out

    def unselectUnit(self):
        self.unit.highlighted = False
        self.unit = None
        self.moveset = None

    def checkStalemate(self):
        for piece in self.turnPieces(False):
            x, y = utils.coordToBoard(piece.x, piece.y)
            self.unit = piece
            moves = piece.moves(self.validateMoves(piece.path(x, y, self.turnPieces(False), self.turnPieces(True))), ["Defend"])
            if len(moves) > 0:
                self.unit = None
                return
        self.unit = None
        self.state = "Stalemate"
    def capture(self, target):
        self.addCapture(target)
        self.turnPieces(True).remove(target)

    def addCapture(self, target):
        caps = self.capWhites if self.turnW else self.capBlacks
        caps.append(target)
        new = []
        def addType(t):
            for piece in caps:
                if isinstance(piece, t):
                    new.append(piece)
                    nX = 150 if self.turnW else 12
                    nY = OFFSET + len(new)*13
                    if len(new) > 8:
                        nX += 10
                        nY -= 8*12
                    piece.x, piece.y = nX, nY
        addType(Pieces.Pawn)
        addType(Pieces.Horse)
        addType(Pieces.Bishop)
        addType(Pieces.Rook)
        addType(Pieces.Queen)

        caps = new

    # Update
    def update(self):
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            out = False
            if self.state == "Chess":
                # There is a piece selected
                if (self.unit != None and not self.check) or (self.check and self.poss.get(self.unit) != None):
                    x, y = utils.coordToBoard(pyxel.mouse_x, pyxel.mouse_y)
                    if x > 7 or x < 0 or y > 7 or y < 0:
                       return False
                    flag = False
                    if self.check:
                        for move in self.poss[self.unit]:
                            x2, y2 = move["pos"]
                            if x == x2 and y == y2:
                                flag = True
                                break
                    # Valid Move
                    if ((self.moveset[y][x] != False and self.moveset[y][x]["type"] != "Defend" and not self.check)
                        or (self.check and flag)):
                        # Capture
                        if self.moveset[y][x]["type"] == "Capture":
                            self.capture(self.moveset[y][x]["target"])
                        # Passant
                        elif self.moveset[y][x]["type"] == "Passant":
                            self.capture(self.moveset[y][x]["target"])
                        elif self.moveset[y][x]["type"] == "Castling":
                            rook = self.moveset[y][x]["Rook"]
                            rook.x, rook.y = utils.boardToCoord(*self.moveset[y][x]["RookTarget"])
                        # Pawn Moving
                        if isinstance(self.unit, Pieces.Pawn):
                            x2, y2 = utils.coordToBoard(self.unit.x,self.unit.y)
                            # Promotion
                            if (y2 == 1 and self.turnW) or (y2 == 6 and not self.turnW):
                                self.state = "Promotion"
                                self.promoted = self.whites.index(self.unit) if self.turnW else self.blacks.index(self.unit)
                            # First Move
                            if abs(y-y2) == 2:
                                self.unit.justMoved = True
                                self.passantU = self.unit
                            elif self.passantU != None and self.passantU.justMoved:
                                self.passantU.justMoved = False
                        self.unit.x, self.unit.y = utils.boardToCoord(x, y)
                        self.turnW = not self.turnW
                        self.unit.moved = True
                        self.unselectUnit()

                        self.check = self.checkCheck(self.turnPieces(True), self.turnPieces(False))

                        # Checkmate
                        if self.check:
                            self.checkCheckmate()
                        else:
                            self.checkStalemate()
                        
                    # Not a Valid Move
                    else:
                        tmp = utils.mousePos(self.turnPieces(False))
                        # Selected same piece
                        if tmp == self.unit:
                            self.unselectUnit()
                        # Another piece selected
                        elif (tmp != None and not self.check) or (self.check and self.poss.get(tmp) != None):
                            self.unit.highlighted = not self.unit.highlighted
                            self.unit = tmp
                            self.unit.highlighted = not self.unit.highlighted
                            self.moveset = self.validateMoves(self.unit.path(*utils.coordToBoard(self.unit.x, self.unit.y), self.turnPieces(False), self.turnPieces(True)))
                # There is not
                else:
                    self.unit = utils.mousePos(self.turnPieces(False))
                    if (self.unit != None and not self.check) or (self.check and self.poss.get(self.unit) != None):
                        self.unit.highlighted = not self.unit.highlighted
                        self.moveset = self.unit.path(*utils.coordToBoard(self.unit.x, self.unit.y), self.turnPieces(False), self.turnPieces(True))
                        self.moveset = self.validateMoves(self.moveset)

            elif self.state == "Promotion":
                x, y = utils.coordToBoard(pyxel.mouse_x, pyxel.mouse_y)
                if y == 4:
                    for i in range(4):
                        if x == i+2:
                            if self.turnW:
                                self.blacks[self.promoted] = self.LAYOUT[i](self.blacks[self.promoted].x, self.blacks[self.promoted].y, False) 
                            else:
                                self.whites[self.promoted] = self.LAYOUT[i](self.whites[self.promoted].x, self.whites[self.promoted].y, True) 
                            self.promoted = None
                            self.state = "Chess"

                            self.check = self.checkCheck(self.turnPieces(True), self.turnPieces(False))
                            if self.check:
                                self.checkCheckmate()
                            break
            elif self.state in ("Checkmate", "Stalemate"):
                return True

            return False
    # Draw
    def draw(self):
        # Clear Screen
        pyxel.cls(0)
        
        # Board
        pyxel.rectb(OFFSET-1, OFFSET-1, TILESIZE*8+2, TILESIZE*8+2, pyxel.COLOR_ORANGE)
        pyxel.rectb(OFFSET-2, OFFSET-2, TILESIZE*8+4, TILESIZE*8+4, pyxel.COLOR_ORANGE)
        toggle = False
        moves = []

        for i in range(8):
            for j in range(8):
                color = pyxel.COLOR_BROWN if toggle else pyxel.COLOR_PEACH
                toggle = not toggle
                if not self.check:
                    if self.moveset != None and self.moveset[j][i] != False and self.moveset[j][i]["type"] == "Capture":
                        color = pyxel.COLOR_RED
                    if self.moveset != None and self.moveset[j][i] != False and self.moveset[j][i]["type"] in ("Passant", "Castling"):
                        moves.append(self.moveset[j][i])
                pyxel.rect(i*TILESIZE+OFFSET, j*TILESIZE+OFFSET, TILESIZE, TILESIZE, color)
                if self.moveset != None and self.moveset[j][i] != False and "Move" in self.moveset[j][i]["type"] and not self.check:
                    x, y = utils.boardToCoord(i, j)
                    pyxel.rect(x+1, y+3, 6, 6, pyxel.COLOR_RED)
            toggle = not toggle

        # Special Moves
        if moves != []:
            for m in moves:
                if m["type"] == "Passant":
                    x, y = utils.boardToCoord(*m["pos"])
                else:
                    x, y = utils.boardToCoord(*m["KingTarget"])
                pyxel.rect(x+1, y+3, 6, 6, pyxel.COLOR_RED)
            
        # Check Moves
        if self.check and self.state != "Checkmate":
            pyxel.text(80, 15, "Check", pyxel.COLOR_RED)
            for piece in self.poss:
                i, j =  utils.coordToBoard(piece.x, piece.y)
                pyxel.rect(i*TILESIZE+OFFSET+1, j*TILESIZE+OFFSET+1, TILESIZE-2, TILESIZE-2, pyxel.COLOR_CYAN)
            if self.poss.get(self.unit) != None:
                    for move in self.poss[self.unit]:
                        x, y = utils.boardToCoord(*move["pos"])
                        if move["type"] != "Capture":
                            pyxel.rect(x+1, y+3, 6, 6, pyxel.COLOR_CYAN)
                        else:
                            pyxel.rect(x-3, y-1, TILESIZE, TILESIZE, pyxel.COLOR_DARKBLUE)

        # Pieces
        for piece in self.whites+self.blacks:
            piece.draw()

        # Captures
        pyxel.rect(149, OFFSET+12, 20 ,8*12+10,  pyxel.COLOR_GRAY)
        pyxel.rect(11, OFFSET+12, 20 ,8*12+10,  pyxel.COLOR_GRAY)
        for piece in self.capWhites+self.capBlacks:
            piece.draw()

        # Promotion Screen
        if self.state == "Promotion":
            for x in range(4):
                pyxel.rect((x+2)*TILESIZE+OFFSET, 3*TILESIZE+OFFSET, TILESIZE, 2*TILESIZE, pyxel.COLOR_GRAY)
                tmp = self.LAYOUT[x](*utils.boardToCoord(x+2, 4), not self.turnW)
                tmp.draw()
            pyxel.text(3*TILESIZE+OFFSET+2, 3*TILESIZE+OFFSET+1, "Choose", pyxel.COLOR_BLACK)
            pyxel.text(2*TILESIZE+OFFSET+10, 3*TILESIZE+OFFSET+7, "Promotion", pyxel.COLOR_BLACK)


        # End Screen
        if self.state in ("Checkmate", "Stalemate"):
            msg = "Checkmate" if self.state == "Checkmate" else "Stalemate"
            pyxel.text(73, 13, msg, pyxel.COLOR_RED)
            if self.state == "Stalemate":
                pyxel.text(84, 20, "Draw", pyxel.COLOR_CYAN)
            else:    
                msg = "White" if not self.turnW else "Black"
                pyxel.text(71, 20, msg + " Wins", pyxel.COLOR_CYAN)
            pyxel.text(55, 160, "Click to continue", pyxel.COLOR_WHITE)
        # Turn
        else:
            msg = "White's Turn" if self.turnW else "Black's Turn"
            pyxel.text(67, 160, msg, pyxel.COLOR_WHITE)