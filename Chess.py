import pyxel
from copy import deepcopy

import Pieces
import utils
from constants import OFFSET, TILESIZE

# Pyxel Init
pyxel.init(180, 180, fps=60)
pyxel.mouse(True)

# Init
whites = []
blacks = []
LAYOUT = [Pieces.Rook, Pieces.Horse, Pieces.Bishop, 
            Pieces.Queen, Pieces.King, Pieces.Bishop,
            Pieces.Horse, Pieces.Rook]

for i in range(8):
    whites.append(Pieces.Pawn(*utils.boardToCoord(i, 6), True))
    whites.append(LAYOUT[i](*utils.boardToCoord(i, 7), True))
    blacks.append(Pieces.Pawn(*utils.boardToCoord(i, 1), False))
    blacks.append(LAYOUT[i](*utils.boardToCoord(i, 0), False))

turnW = True
moveset = None
unit = None
promoted = None
passantU = None
state = "Chess"
check = False
poss = None

# Macro
turnPieces = lambda inv: whites if (turnW and not inv) or (not turnW and inv) else blacks

def checkCheck(enemyPieces, allyPieces):
    check = False
    danger = []
    for piece in enemyPieces:
        x2, y2 = utils.coordToBoard(piece.x, piece.y)
        toAdd = piece.moves(piece.path(x2, y2, enemyPieces, allyPieces), ["Defend", "Move", "CMove", "PMove"])
        for a in toAdd:
            if isinstance(a["target"], Pieces.King):
                check = True
                danger.append(a)
    return check

def castling(king, moveset, allyPieces, enemyPieces):
        def rookLogic(rook, const):
            flag = False
            backupX, backupY = king.x, king.y
            for i in range(2):
                king.x += const*TILESIZE
                flag = checkCheck(enemyPieces, allyPieces)
                if flag:
                    break
            king.x, king.y = backupX, backupY
            if not flag:
                x, y = utils.coordToBoard(king.x, king.y)
                moveset[y][x+2*const] = {"type": "Castling", "Rook": rook, "RookTarget" : (x+const, y),
                                    "King": king, "KingTarget" : (x+2*const, y)}
        if not king.moved:
            lRook, rRook = None, None
            for piece in allyPieces:
                if isinstance(piece, Pieces.Rook) and not piece.moved:
                    if piece.x < king.x:
                        lRook = piece
                    else:
                        rRook = piece
            if lRook != None:
                rookLogic(lRook, -1)
            if rRook != None:
                rookLogic(rRook, 1)
        return moveset

def checkCheckmate():
    global poss
    ally = deepcopy(whites) if turnW else deepcopy(blacks)
    enemy = deepcopy(whites) if not turnW else deepcopy(blacks)
    poss = {}
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
                flag = checkCheck(tEnemy, ally)
            else:
                flag = checkCheck(enemy, ally)
            if not flag:
                pieceToAdd = whites[ally.index(piece)] if turnW else blacks[ally.index(piece)]
                if poss.get(pieceToAdd) == None:
                    poss[pieceToAdd] = [p]
                else:
                    poss[pieceToAdd].append(p)

            piece.x, piece.y = utils.boardToCoord(xi, yi)

    if len(poss) > 0:
        print("Check")
    else:
        print("Checkmate!")
        print("Black Won!" if turnW else "White Won!")
        raise SystemExit

def validateMoves(moves):
    if isinstance(unit, Pieces.King):
        out = castling(unit, unit.forbid(moves, turnPieces(False), turnPieces(True)), turnPieces(False), turnPieces(True))
    else:
        out = []
        for row in moves:
            toAdd = []
            for m in row:
                if not m:
                    toAdd.append(False)
                    continue
                enemy = whites if not turnW else blacks
                backup = unit.x, unit.y
                unit.x, unit.y = utils.boardToCoord(*m["pos"])
                if m["type"] == "Capture":
                    t = enemy.index(m["target"])
                    tEnemy = enemy[:t] + enemy[t+1:]
                    flag = checkCheck(tEnemy, turnPieces(False))
                else:
                    flag = checkCheck(enemy, turnPieces(False))
                unit.x, unit.y = backup
                if flag:
                    toAdd.append(False)
                else:
                    toAdd.append(m)
            out.append(toAdd)
    if unit.moves(out, ["CMove", "Defend"]) == []:
        unselectUnit()
    return out

def unselectUnit():
    global unit, moveset
    unit.highlighted = False
    unit = None
    moveset = None

def capture(target):
    toRemove = whites if not turnW else blacks
    toRemove.remove(target)

# Update
def update():
    if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
        global unit, turnW, moveset, passantU, check, poss, state, promoted
        if state == "Chess":
            # There is a piece selected
            if (unit != None and not check) or (check and poss.get(unit) != None):
                x, y = utils.coordToBoard(pyxel.mouse_x, pyxel.mouse_y)
                flag = False
                if check:
                    for move in poss[unit]:
                        x2, y2 = move["pos"]
                        if x == x2 and y == y2:
                            flag = True
                            break
                # Valid Move
                if ((moveset[y][x] != False and moveset[y][x]["type"] != "Defend" and not check)
                    or (check and flag)):
                    # Capture
                    if moveset[y][x]["type"] == "Capture":
                        capture(moveset[y][x]["target"])
                    # Passant
                    elif moveset[y][x]["type"] == "Passant":
                        capture(moveset[y][x]["target"])
                    elif moveset[y][x]["type"] == "Castling":
                        rook = moveset[y][x]["Rook"]
                        rook.x, rook.y = utils.boardToCoord(*moveset[y][x]["RookTarget"])
                    # Pawn Moving
                    if isinstance(unit, Pieces.Pawn):
                        x2, y2 = utils.coordToBoard(unit.x,unit.y)
                        # Promotion
                        if (y2 == 1 and turnW) or (y2 == 6 and not turnW):
                            state = "Promotion"
                            promoted = whites.index(unit) if turnW else blacks.index(unit)
                        # First Move
                        if abs(y-y2) == 2:
                            unit.justMoved = True
                            passantU = unit
                        elif passantU != None and passantU.justMoved:
                            passantU.justMoved = False
                    unit.x, unit.y = utils.boardToCoord(x, y)
                    turnW = not turnW
                    unit.moved = True
                    unselectUnit()

                    check = checkCheck(turnPieces(True), turnPieces(False))

                    # Checkmate
                    if check:
                        checkCheckmate()
                    
                # Not a Valid Move
                else:
                    tmp = utils.mousePos(turnPieces(False))
                    # Selected same piece
                    if tmp == unit:
                        unselectUnit()
                    # Another piece selected
                    elif (tmp != None and not check) or (check and poss.get(tmp) != None):
                        unit.highlighted = not unit.highlighted
                        unit = tmp
                        unit.highlighted = not unit.highlighted
                        moveset = validateMoves(unit.path(*utils.coordToBoard(unit.x, unit.y), turnPieces(False), turnPieces(True)))
            # There is not
            else:
                unit = utils.mousePos(turnPieces(False))
                if (unit != None and not check) or (check and poss.get(unit) != None):
                    unit.highlighted = not unit.highlighted
                    moveset = unit.path(*utils.coordToBoard(unit.x, unit.y), turnPieces(False), turnPieces(True))
                    moveset = validateMoves(moveset)

        elif state == "Promotion":
            x, y = utils.coordToBoard(pyxel.mouse_x, pyxel.mouse_y)
            if y == 4:
                for i in range(4):
                    if x == i+2:
                        if turnW:
                            blacks[promoted] = LAYOUT[i](blacks[promoted].x, blacks[promoted].y, False) 
                        else:
                            whites[promoted] = LAYOUT[i](whites[promoted].x, whites[promoted].y, True) 
                        promoted = None
                        state = "Chess"

                        check = checkCheck(turnPieces(True), turnPieces(False))
                        if check:
                            checkCheckmate()

                        break
# Draw
def draw():
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
            if not check:
                if moveset != None and moveset[j][i] != False and moveset[j][i]["type"] == "Capture":
                    color = pyxel.COLOR_RED
                if moveset != None and moveset[j][i] != False and moveset[j][i]["type"] in ("Passant", "Castling"):
                    moves.append(moveset[j][i])
            pyxel.rect(i*TILESIZE+OFFSET, j*TILESIZE+OFFSET, TILESIZE, TILESIZE, color)
            if moveset != None and moveset[j][i] != False and "Move" in moveset[j][i]["type"] and not check:
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
    if check:
        for piece in poss:
            i, j =  utils.coordToBoard(piece.x, piece.y)
            pyxel.rect(i*TILESIZE+OFFSET+1, j*TILESIZE+OFFSET+1, TILESIZE-2, TILESIZE-2, pyxel.COLOR_CYAN)
        if poss.get(unit) != None:
                for move in poss[unit]:
                    x, y = utils.boardToCoord(*move["pos"])
                    if move["type"] != "Capture":
                        pyxel.rect(x+1, y+3, 6, 6, pyxel.COLOR_CYAN)
                    else:
                        pyxel.rect(x-3, y-1, TILESIZE, TILESIZE, pyxel.COLOR_DARKBLUE)

    # Pieces
    for piece in whites+blacks:
        piece.draw()

    # Turn
    msg = "White's Turn" if turnW else "Black's Turn"
    pyxel.text(65, 160, msg, pyxel.COLOR_WHITE)

    # Promotion Screen
    if state == "Promotion":
        for x in range(4):
            pyxel.rect((x+2)*TILESIZE+OFFSET, 3*TILESIZE+OFFSET, TILESIZE, 2*TILESIZE, pyxel.COLOR_GRAY)
            tmp = LAYOUT[x](*utils.boardToCoord(x+2, 4), not turnW)
            tmp.draw()
        pyxel.text(3*TILESIZE+OFFSET+2, 3*TILESIZE+OFFSET+1, "Choose", pyxel.COLOR_BLACK)
        pyxel.text(2*TILESIZE+OFFSET+10, 3*TILESIZE+OFFSET+7, "Promotion", pyxel.COLOR_BLACK)

# Game Load
pyxel.run(update, draw)