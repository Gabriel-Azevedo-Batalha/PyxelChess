import pyxel

import Pieces
import utils
from constants import OFFSET, TILESIZE

# Pyxel Init
pyxel.init(180, 180, fps=60)
pyxel.mouse(True)

# Init
whites = utils.initSide(True)
blacks = utils.initSide(False)

# Update
def update():
    # To Do
    return
# Draw
def draw():

    # Clear Screen
    pyxel.cls(0)
    
    # Board
    pyxel.rectb(OFFSET-1, OFFSET-1, TILESIZE*8+2, TILESIZE*8+2, pyxel.COLOR_ORANGE)
    pyxel.rectb(OFFSET-2, OFFSET-2, TILESIZE*8+4, TILESIZE*8+4, pyxel.COLOR_ORANGE)
    toggle = False
    for i in range(8):
        for j in range(8):
            color = pyxel.COLOR_BROWN if toggle else pyxel.COLOR_PEACH
            toggle = not toggle
            pyxel.rect(i*TILESIZE+OFFSET, j*TILESIZE+OFFSET, TILESIZE, TILESIZE, color)
        toggle = not toggle

    # Pieces
    for piece in whites:
        piece.draw()
    for piece in blacks:
        piece.draw()

# Game Load
pyxel.run(update, draw)