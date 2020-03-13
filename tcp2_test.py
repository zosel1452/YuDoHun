from socket import *

from select import select

import sys

 

HOST = '192.168.0.10'

PORT = 8888

BUFSIZE = 1024

while True:

   # clientSocket = socket(AF_INET, SOCK_STREAM)

    try:
        clientSocket = socket(AF_INET,SOCK_STREAM)
        clientSocket.connect((HOST,PORT))
        msg = input()
        #clientSocket.send(msg.encode(encoding = 'UTF-8',errors = 'strict'))
        clientSocket.sendall(bytes("datad%s\n"%msg, 'UTF-8'))
        print('Send : Hello, Server!\n')
        data = clientSocket.recv(1024)
        print(data.decode())
        clientSocket.close()

    except Exception as e:
        print(e)
        clientSocket.close()









