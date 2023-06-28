import pyxel

class Menu():
    def __init__(self):
        self.active = True

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            x, y = pyxel.mouse_x, pyxel.mouse_y
            if x >= 68 and x <= 114 and y >= 124 and y <= 140:
                self.active = False
    
    def draw(self):
        pyxel.load("assets/assets.pyxres")
        pyxel.cls(0)
        pyxel.blt(45, 20, 0, 16, 0, 90, 60, pyxel.COLOR_YELLOW)
        pyxel.blt(68, 124, 0, 0, 80, 44, 16, pyxel.COLOR_YELLOW)
