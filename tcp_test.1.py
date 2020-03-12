from socket import *
from select import select
import sys

HOST = '192.168.0.10'
PORT = 8888
BUFSIZE = 1024

clientSocket = socket(AF_INET, SOCK_STREAM)

try:
   clientSocket.connect((HOST,PORT))
   clientSocket.sendall(bytes("Hello, Server!\n", 'UTF-8'))
   print('Send : Hello, Server!\n')
   data = clientSocket.recv(1024)
   print(data.decode())
   clientSocket.close()
except Exception as e:
   print(e)
