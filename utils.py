import Pieces
from constants import OFFSET, TILESIZE, LAYOUT

def boardToCoord(boardX, boardY):
    x = OFFSET + boardX*TILESIZE + 3
    y = OFFSET + boardY*TILESIZE + 1
    return x, y

def initSide(white):
    side = []
    y = 6 if white else 1
    mod = 1 if white else -1

    for i in range(8):
        side.append(Pieces.Pawn(*boardToCoord(i, y), white))
        side.append(LAYOUT[i](*boardToCoord(i, y+mod), white))

    return side