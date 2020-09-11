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


def add_coordinates(board, black=False):
    b = board.unicode(invert_color=True).split('\n')
    coord_board = []
    i = 8
    for row in b:
        coord_board.append(str(i) + ' ' + row)
        i -= 1
    if black:
        coord_board.insert(0, '  A B C D E F G H')
    else:
        coord_board.append('  A B C D E F G H')
    return '\n'.join(coord_board)


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    board = chess.Board()
    s.connect(('127.0.0.1', 6789))
    print(s.recv(4096).decode('utf-8'))  # 'You are in queue' message
    color = s.recv(4096).decode('utf-8')
    print(color + '\n')
    game_on = True

    if color.endswith('white'):
        while game_on:
            print(add_coordinates(board), end='\n\n')
            white_move = move()
            print(add_coordinates(board), end='\n\n')
            s.send(bytes(white_move.uci(), 'utf-8'))
            if board.is_checkmate():
                print('You win')
                break
            black_move = s.recv(4096).decode('utf-8')
            board.push_uci(black_move)
            print(f'Black played {black_move}')
            if board.is_checkmate():
                print('You lose')
                s.send(bytes('lost', 'utf-8'))
                break

    elif color.endswith('black'):
        while game_on:
            white_move = s.recv(4096).decode('utf-8')
            board.push_uci(white_move)
            print(f'White played {white_move}')
            print(add_coordinates(board, True)[::-1], end='\n\n')
            if board.is_checkmate():
                print('You lose')
                s.send(bytes('lost', 'utf-8'))
                break
            black_move = move()
            s.send(bytes(black_move.uci(), 'utf-8'))
            print(add_coordinates(board, True)[::-1], end='\n\n')
            if board.is_checkmate():
                print('You win')
                break
