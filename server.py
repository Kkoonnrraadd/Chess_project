import socket
import threading
import logging
import sys
import logging.handlers
from collections import deque
# import syslog
# syslog.syslog("This is a test message")
# syslog.syslog(syslog.LOG_INFO, "Test message at INFO priority")
from logging import config

# try:
#     import syslog
#     _LOG_TO_SYSLOG = {
#         logging.DEBUG: syslog.LOG_DEBUG,
#         logging.INFO: syslog.LOG_INFO,
#         logging.WARNING: syslog.LOG_WARNING,
#         logging.ERROR: syslog.LOG_ERR,
#         logging.CRITICAL: syslog.LOG_CRIT
#     }
# except ImportError:
#     _LOG_TO_SYSLOG = {}
#
#
# def send_to_logs(self):
#     """Send to logs: either GAE logs (for appengine) or syslog."""
#     if not self._passed_rate_limit('logs'):
#         return self
#
#     logging.log(self.severity, self.message)
#     try:
#         syslog_priority = self._mapped_severity(_LOG_TO_SYSLOG)
#         syslog.syslog(syslog_priority)
#     except (NameError, KeyError) as e:
#         syslog.LOG_ERR(e)
##########################################################################################
log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)

handler = logging.handlers.SysLogHandler(address = './log')

formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
handler.setFormatter(formatter)

log.addHandler(handler)

####################################################################################3
### nr.1 wywala ten sam blad dla obu
###AttributeError: 'SysLogHandler' object has no attribute 'socket'###
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '%(levelname)s %(module)s P%(process)d T%(thread)d %(message)s'
#             },
#         },
#     'handlers': {
#         'stdout': {
#             'class': 'logging.StreamHandler',
#             'stream': sys.stdout,
#             'formatter': 'verbose',
#             },
#         'sys-logger6': {
#             'class': 'logging.handlers.SysLogHandler',
#             'address': './log',
#             'facility': "local6",
#             'formatter': 'verbose',
#             },
#         },
#     'loggers': {
#         'my-logger': {
#             'handlers': ['sys-logger6','stdout'],
#             'level': logging.DEBUG,
#             'propagate': True,
#             },
#         }
#     }
#
# config.dictConfig(LOGGING)
# logger = logging.getLogger("my-logger")

#######################################################################################

# nr.2 same
#my_logger = logging.getLogger()
#my_logger.setLevel(logging.DEBUG)
#handler = logging.handlers.SysLogHandler(address = './log.log')
#my_logger.addHandler(handler)

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
    # my_logger = logging.getLogger('MyLogger')
    # my_logger.setLevel(logging.DEBUG)
    # handler = logging.handlers.SysLogHandler()
    # my_logger.addHandler(handler)
    # file_handler = logging.FileHandler(filename='./examplee.log')

    queue = deque([])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 6789))
    s.listen()

    while True:
        conn, address = s.accept()
        logging.debug(f'Connection from {address} accepted')
        # logger.debug(f'Connection from {address} accepted')
        conn.send(bytes('You are in queue', 'utf-8'))
        queue.append(conn)
        if len(queue) >= 2:
            threading.Thread(group=None, target=game, args=(queue.popleft(), queue.popleft())).start()
