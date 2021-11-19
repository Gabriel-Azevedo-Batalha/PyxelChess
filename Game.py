import Chess
import pyxel
import Menu

# Pyxel Init
pyxel.init(180, 180, fps=60)
pyxel.mouse(True)

# Init
chess =  Chess.Chess()
menu = Menu.Menu()

def update():
    if menu.active:
        menu.update()
    elif chess.update():
        menu.active = True
        chess.__init__()
def draw():
    if menu.active:
        menu.draw()
    else:
        chess.draw()
# Game Load
pyxel.run(update, draw)