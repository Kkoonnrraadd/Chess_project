# TODO: wszystkie legal_moves
# Na razie jest tak, że pozycja jest zarówno w Board i każda figura ma w atrybutach
# Jest to niepotrzebna redundacja pewnie, ale na razie tak bym zostawił
# Zobaczymy jak to potem wyjdzie co jest potrzebne a co nie

WHITE = 0
BLACK = 1
global potential_moves # jakas zmienna jeszcze nie wiem co to bedzie

def which_color(color):
    if color == 1:
        return 'Black'
    elif color == 0:
        return 'White'
    return None

# Pewnie niepotrzebne jednak będzie
# class Position:
#     """Bierze pozycję jako string np. 'a1', 'b4'"""
#
#     def __init__(self, position):
#         self.rank = ord(position[0])
#         self.file = int(position[1])
#
#     def __str__(self):
#         return chr(self.rank) + str(self.file)
#
#     def is_valid(self, new_position):
#         try:
#             if 97 <= ord(new_position[0]) <= 104 and 1 <= int(new_position[1]) <= 8:
#                 return True
#         except ValueError:
#             pass
#         return False
#
#     def move(self, new_position):
#         if self.is_valid(new_position):
#             self.rank = ord(new_position[0])
#             self.file = int(new_position[1])
#             return True
#         return False
#


class Piece:

    def __init__(self, color, file, rank):
        self.color = color
        self.file = file
        self.rank = rank

    def __repr__(self):
        color = which_color(self.color)
        return color + ' ' + self.__class__.__name__


class Board:

    def __init__(self):
        self.board = [[None] * 8 for x in range(0, 8)]
        self.standard_chess()

    def standard_chess(self):
        placement = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i in range(0, 8):
            # 97 is code for 'a'
            self.board[0][i] = placement[i](WHITE, chr(97 + i), '1')
            self.board[1][i] = Pawn(WHITE, chr(97 + i), '2')
            self.board[6][i] = Pawn(BLACK, chr(97 + i), '7')
            self.board[7][i] = placement[i](BLACK, chr(97 + i), '8')

    def __repr__(self):
        return str(self.board)


class King(Piece):
    def legal_moves(self, new_position):
        potential_moves += [(x + 1, y),(x + 1, y + 1),(x, y + 1),(x - 1, y + 1),(x - 1, y),(x - 1, y - 1),(x, y - 1),(x + 1, y - 1)]
        pass


class Queen(Piece): # to moze sie ruszac wszedzie to kombinacja bishop i rook funckji
    def legal_moves(self, new_position):
        move = [(x + j, y + i) for i,j in range(1, 8) if 0 <= x < 8 and 0 <= y < 8]
        
        pass


class Rook(Piece): # znalazlem cos takiego dla xy jaki nasze pozycje np.b3
    def legal_moves(self, new_position):
        u = [(x, y + i) for i in range(1, 8) if 0 <= x < 8 and 0 <= y < 8]
        d = [(x, y - i) for i in range(1, 8) if 0 <= x < 8 and 0 <= y < 8]
        l = [(x - i, y) for i in range(1, 8) if 0 <= x < 8 and 0 <= y < 8]
        r = [(x + i, y) for i in range(1, 8) if 0 <= x < 8 and 0 <= y < 8]
        potential_moves += u + d + l + r
        pass


class Bishop(Piece):
    def legal_moves(self, new_position):
        ur = [(x + i, y + i) for i in range(1, 8) if 0 <= x < 8 and 0 <= y < 8]
        dr = [(x + i, y - i) for i in range(1, 8) if 0 <= x < 8 and 0 <= y < 8]
        ul = [(x - i, y + i) for i in range(1, 8) if 0 <= x < 8 and 0 <= y < 8]
        dl = [(x - i, y - i) for i in range(1, 8) if 0 <= x < 8 and 0 <= y < 8]
        potential_moves += ur + dr + ul + dl
        pass


class Knight(Piece):
    def legal_moves(self, new_position):
        potential_moves += [(x + 2, y + 1), (x + 2, y - 1)
            , (x + 1, y + 2), (x + 1, y - 2)
            , (x - 2, y - 1), (x - 2, y + 1)
            , (x - 1, y + 2), (x - 1, y - 2)]
        pass


class Pawn(Piece):
    def legal_moves(self, new_position):
        if which_color(1) and x == 6:
            potential_moves = [(x - 2, y)]

        elif which_color(0) and x == 1:
            potential_moves = [(x + 2, y)]

        elif which_color(1):
            potential_moves = [(x - 1, y)]

        elif which_color(0):
            potential_moves = [(x + 1, y)]

        pass
