import socket
import ssl

from server import HOST as SERVER_HOST
from server import PORT as SERVER_PORT
from server import SERVER_COMMON_NAME

ATTACKER_CERT = './attacker/attacke.crt'
ATTACKER_KEY = './attacker/attacker.key'

context = ssl.create_default_context(
  ssl.Purpose.SERVER_AUTH,
)
context.load_cert_chain(certfile=ATTACKER_CERT, keyfile=ATTACKER_KEY)

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