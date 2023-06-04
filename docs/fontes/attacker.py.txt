import socket
import ssl

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client = context.wrap_socket(
  client, server_hostname=SERVER_HOST
)

client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if __name__ == '__main__':
  client.connect((SERVER_HOST, SERVER_PORT))
  
  client.sendall('Hello babyyyyy'.encode('utf-8'))
  
  client.close()