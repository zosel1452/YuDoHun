######## 라즈베리파이 코드 #######
##### 데이터를 받는 부분(서버) ######

import socket
import sys

HOST = ''   #서버 지정 x pc 에서 여기의 ip 주소를 입력 하면 됨
PORT = 8888 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('socket created')

try:
   s.bimd((HOST, PORT))
except socket.error as msg:
   print('bind Failed. error code : ' +str(msg[0]) + ' message ' + msg[1])
   sys.exit()

print(' socket bind complete ')


while 1:
   s.listen(1)
   conn, addr = s.accept()

   data = conn.recv(1024)
   
   if not data:
      break
   conn.sendall(data)
   print(data.decode())

conn.close()
s.close()
