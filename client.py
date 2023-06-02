import socket
import ssl

from server import HOST as SERVER_HOST
from server import PORT as SERVER_PORT
from server import SERVER_COMMON_NAME
from server import SERVER_CERT

CLIENT_CERT = './client/client.crt'
CLIENT_KEY = './client/client.key'

context = ssl.create_default_context(
  ssl.Purpose.SERVER_AUTH,
  cafile=SERVER_CERT
)
context.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client = context.wrap_socket(
    client,
    server_side=False,
    server_hostname=SERVER_COMMON_NAME
)

if __name__ == '__main__':
  client.connect((SERVER_HOST, SERVER_PORT))
  
  client.send('Hello babyyyyy'.encode('utf-8'))
  
  client.close()