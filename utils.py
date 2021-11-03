import pyxel
from constants import OFFSET, TILESIZE

def boardToCoord(boardX, boardY):
    x = OFFSET + boardX*TILESIZE + 3
    y = OFFSET + boardY*TILESIZE + 1
    return x, y
def coordToBoard(x, y):
    boardX = (x-OFFSET)//TILESIZE
    boardY = (y-OFFSET)//TILESIZE
    return boardX, boardY
def mousePos(pieces):
    for piece in pieces:
        if coordToBoard(pyxel.mouse_x, pyxel.mouse_y) == coordToBoard(piece.x, piece.y):
            return piece
    return None
