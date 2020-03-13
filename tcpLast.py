from socket import *

from select import select

import sys

import time 

HOST = '192.168.43.25'

PORT = 8888

BUFSIZE = 1024


while True:
    
    
   # clientSocket = socket(AF_INET, SOCK_STREAM)

    try:
        clientSocket = socket(AF_INET,SOCK_STREAM)
        clientSocket.connect((HOST,PORT))
        msg = input()
        
        
        #clientSocket.send(msg.encode(encoding = 'UTF-8',errors = 'strict'))
        clientSocket.sendall(bytes("time : %s\n"%msg, 'UTF-8'))
        print('Send : Hello, Server!\n')
        data = clientSocket.recv(1024)
        print(data.decode())
        clientSocket.close()

    except Exception as e:
        print(e)
        clientSocket.close()
        print("cant open")
        









