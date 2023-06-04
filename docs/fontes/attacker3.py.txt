import socket
import ssl

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080
SERVER_COMMON_NAME = 'astora'
SERVER_CERT = './server/server.crt'

ATTACKER_CERT = './attacker/attacke.crt'
ATTACKER_KEY = './attacker/attacker.key'

context = ssl.create_default_context(
  ssl.Purpose.SERVER_AUTH,
  cafile=SERVER_CERT
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