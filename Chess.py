from typing import Tuple
import pyxel

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


# Update
def update():
    if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
        global unit
        global turnW
        global moveset

        # There is a piece selected
        if unit != None:
            x, y = utils.coordToBoard(pyxel.mouse_x, pyxel.mouse_y)
            # Valid Move
            if moveset[y][x] != False:
                # Capture
                if isinstance(moveset[y][x], Pieces.Piece):
                    if turnW:
                        blacks.remove(moveset[y][x])
                    else:
                        whites.remove(moveset[y][x])
                # Passant
                elif isinstance(moveset[y][x], Tuple):
                    if turnW:
                        blacks.remove(moveset[y][x][1])
                    else:
                        whites.remove(moveset[y][x][1])
                # Pawn Moving
                if isinstance(unit, Pieces.Pawn):
                    x2, y2 = utils.coordToBoard(unit.x,unit.y)
                    # Promotion
                    """ if y2 == 0 or y2 == 7:
                        PromotionSelector """
                    if abs(y-y2) == 2:
                        unit.justMoved = True
                    elif unit.justMoved:
                        unit.justMoved = False
                unit.x, unit.y = utils.boardToCoord(x, y)
                unit.highlighted = not unit.highlighted
                turnW = not turnW
                unit.moved = True
                unit = None
                moveset = None
            # Not a Valid Move
            else:
                tmp = utils.mousePos(whites) if turnW else utils.mousePos(blacks)
                # Selected same piece
                if tmp == unit:
                    unit.highlighted = not unit.highlighted
                    unit = None
                    moveset = None
                # Another piece selected
                elif tmp != None:
                    unit.highlighted = not unit.highlighted
                    unit = tmp
                    unit.highlighted = not unit.highlighted
                    moveset = unit.path(*utils.coordToBoard(unit.x, unit.y), whites if turnW else blacks, whites if not turnW else blacks)
        # There is not
        else:
            unit = utils.mousePos(whites) if turnW else utils.mousePos(blacks)
            if unit != None:
                unit.highlighted = not unit.highlighted
                moveset = unit.path(*utils.coordToBoard(unit.x, unit.y), whites if turnW else blacks, whites if not turnW else blacks)
    return
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
            if moveset != None and isinstance(moveset[j][i], Pieces.Piece):
                color = pyxel.COLOR_RED
            if moveset != None and isinstance(moveset[j][i], Tuple):
                moves.append(moveset[j][i])
            pyxel.rect(i*TILESIZE+OFFSET, j*TILESIZE+OFFSET, TILESIZE, TILESIZE, color)
            if moveset != None and moveset[j][i] == True:
                x, y = utils.boardToCoord(i, j)
                pyxel.rect(x+1, y+3, 6, 6, pyxel.COLOR_RED)
        toggle = not toggle

    # Special Moves
    if moves != []:
        for m in moves:
            x, y = utils.boardToCoord(*m[0])
            pyxel.rect(x+1, y+3, 6, 6, pyxel.COLOR_RED)

    # Pieces
    for piece in whites:
        piece.draw()
    for piece in blacks:
        piece.draw()

    # Turn
    msg = "White's Turn" if turnW else "Black's Turn"
    pyxel.text(65, 160, msg, pyxel.COLOR_WHITE)

# Game Load
pyxel.run(update, draw)