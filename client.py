import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.131', 6789))
print(s.recv(4096).decode('utf-8'))
print(s.recv(4096).decode('utf-8'))
