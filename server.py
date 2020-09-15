import socket
import threading
import logging
import logging.handlers
from collections import deque


def game(white, black):
    white.send(bytes('You are white', 'utf-8'))
    black.send(bytes('You are black', 'utf-8'))
    while True:
        white_move = white.recv(4096)
        if white_move.decode('utf-8') == 'lost':
            break
        black.send(white_move)
        black_move = black.recv(4096)
        if black_move.decode('utf-8') == 'lost':
            break
        white.send(black_move)


if __name__ == '__main__':
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.DEBUG)
    handler = logging.handlers.SysLogHandler(address="/dev/log")
    my_logger.addHandler(handler)

    queue = deque([])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 6789))
    s.listen()

    while True:
        conn, address = s.accept()
        my_logger.debug(f'Connection from {address} accepted')
        conn.send(bytes('You are in queue', 'utf-8'))
        queue.append(conn)
        if len(queue) >= 2:
            threading.Thread(group=None, target=game, args=(queue.popleft(), queue.popleft())).start()
