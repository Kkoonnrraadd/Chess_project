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
        pass


class Queen(Piece):
    def legal_moves(self, new_position):
        pass


class Rook(Piece): 
    def legal_moves(self, new_position):
        pass


class Bishop(Piece):
    def legal_moves(self, new_position):
        pass


class Knight(Piece):
    def legal_moves(self, new_position):
        pass


class Pawn(Piece):
    def legal_moves(self, new_position):
        pass
