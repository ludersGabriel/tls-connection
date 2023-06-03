import socket, os
from threading import Thread

from dotenv import load_dotenv

MAX_TCP_SIZE = 2 ** 16 - 1024

def handle_send(socket_in, socket_out, fromClient = False):
  assert isinstance(socket_in, socket.socket)
  assert isinstance(socket_out, socket.socket)
  
  if not fromClient:
    while True:
        try:
            socket_out.sendall(socket_in.recv(MAX_TCP_SIZE))
        except:
            break
  else:
    while True:
        try:
          data = socket_in.recv(MAX_TCP_SIZE)
          
          data = bytearray(data)
          
          data[len(data) - 1] = data[len(data) - 1] ^ 1
                    
          socket_out.sendall(bytes(data))
        except:
          break

if __name__ == '__main__':
  load_dotenv()
  MAN_HOST = os.getenv('MAN_HOST')
  MAN_PORT = int(os.getenv('MAN_PORT'))
  
  SERVER_HOST = os.getenv('HOST')
  SERVER_PORT = int(os.getenv('PORT'))
  
  listener_socket = socket.socket(
      socket.AF_INET, socket.SOCK_STREAM
  )
  listener_socket.bind((MAN_HOST, MAN_PORT))
  listener_socket.listen(5)
  
  server_socket = socket.socket(
      socket.AF_INET, socket.SOCK_STREAM
  )
  server_socket.connect((SERVER_HOST, SERVER_PORT))
  
  client_socket, address = listener_socket.accept()
  Thread(target=handle_send, args=(client_socket, server_socket, True)).start()
  Thread(target=handle_send, args=(server_socket, client_socket)).start()

