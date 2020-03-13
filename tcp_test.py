#python3

import socket

HOST = '192.168.0.10'
PORT = 8888

while True:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((HOST,PORT))

    msg = input()
    s.send(msg.encode(encoding = 'utf_8',errors = 'strict'))
    data = s.recv(1024)


s.close()
