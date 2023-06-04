import socket, os
from threading import Thread

from dotenv import load_dotenv

# Maximum size of TCP packets
MAX_TCP_SIZE = 2 ** 16 - 1024

def handle_send(socket_in, socket_out, fromClient = False):
  # Verify that the sockets instances were created properly
  assert isinstance(socket_in, socket.socket)
  assert isinstance(socket_out, socket.socket)
  
  # Server -> Client flow
  if not fromClient:
    while True:
        try:
            socket_out.sendall(socket_in.recv(MAX_TCP_SIZE))
        except:
            break
  # Client -> Server flow
  else:
    while True:
        try:
          data = socket_in.recv(MAX_TCP_SIZE)
          
          data = bytearray(data)
          # Invert the last bit of our data using XOR
          data[len(data) - 1] = data[len(data) - 1] ^ 1
                    
          socket_out.sendall(bytes(data))
        except:
          break

if __name__ == '__main__':
  # Load environment variables of .env
  load_dotenv()
  MAN_HOST = os.getenv('MAN_HOST')
  MAN_PORT = int(os.getenv('MAN_PORT'))
  
  SERVER_HOST = os.getenv('HOST')
  SERVER_PORT = int(os.getenv('PORT'))
  
  # Creates a TCP socket with ipv4
  listener_socket = socket.socket(
      socket.AF_INET, socket.SOCK_STREAM
  )

  # Binds the socket with a port
  listener_socket.bind((MAN_HOST, MAN_PORT))
  listener_socket.listen(5)
  
  # Creates a TCP socket with ipv4 to connect to the server
  server_socket = socket.socket(
      socket.AF_INET, socket.SOCK_STREAM
  )
  server_socket.connect((SERVER_HOST, SERVER_PORT))
  
  # Use the listener socket to listen to the client
  client_socket, address = listener_socket.accept()

  # Creates two threads to: client -> server flow and server -> client flow
  Thread(target=handle_send, args=(client_socket, server_socket, True)).start()
  Thread(target=handle_send, args=(server_socket, client_socket)).start()

