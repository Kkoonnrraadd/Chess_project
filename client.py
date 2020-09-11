import socket
import chess


def move():
    while True:
        try:
            uci = input('Type a move eg. e2e4: ')
            moved = board.push_uci(uci)
            return moved
        except ValueError:
            print('Illegal move')

# def print_board(board):
#     b = board.unicode().split()
#     for square in b:
#         square = '.' if square == '\u2b58' else square


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    board = chess.Board()
    s.connect(('127.0.0.1', 6789))
    print(s.recv(4096).decode('utf-8'))  # 'You are in queue' message
    color = s.recv(4096).decode('utf-8')
    print(color)
    game_on = True

    if color.endswith('white'):
        while game_on:
            print(board.unicode(invert_color=True), end='\n\n')
            white_move = move()
            s.send(bytes(white_move.uci(), 'utf-8'))
            if board.is_checkmate():
                print('You win')
            black_move = s.recv(4096).decode('utf-8')
            board.push_uci(black_move)
            print(board.unicode(invert_color=True), end='\n\n')
            if board.is_checkmate():
                print('You lose')
                s.send(bytes('lost', 'utf-8'))

    elif color.endswith('black'):
        while game_on:
            white_move = s.recv(4096).decode('utf-8')
            board.push_uci(white_move)
            print(board.unicode(invert_color=True)[::-1], end='\n\n')
            if board.is_checkmate():
                print('You lose')
                s.send(bytes('lost', 'utf-8'))
                break
            black_move = move()
            s.send(bytes(black_move.uci(), 'utf-8'))
            print(board.unicode(invert_color=True)[::-1], end='\n\n')
            if board.is_checkmate():
                print('You win')
