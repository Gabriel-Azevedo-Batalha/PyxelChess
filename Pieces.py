import pyxel


class Piece():
    def __init__(self, x, y, white):
        if white:
           self.v = 0
        else:
            self.v = 8
        self.x = x
        self.y = y
    def draw(self):
        pyxel.load("assets.pyxres")
        pyxel.blt(self.x, self.y, 0, self.v, self.u, 8, 12, pyxel.COLOR_YELLOW)

class Pawn(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.u = 0
    def draw(self):
        super().draw()

class Rook(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.u = 12
    def draw(self):
        super().draw()

class Horse(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.u = 24
    def draw(self):
        super().draw()

class Bishop(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.u = 36
    def draw(self):
        super().draw()

class King(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.u = 48
    def draw(self):
        super().draw()

class Queen(Piece):
    def __init__(self, x, y, white):
        super().__init__(x, y, white)
        self.u = 60
    def draw(self):
        super().draw()