import socket
import ssl

from server import HOST as SERVER_HOST
from server import PORT as SERVER_PORT

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

context.load_verify_locations('certificate.crt')
context.load_cert_chain(certfile='certificate.crt', keyfile='server.key')
context.check_hostname = False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client = context.wrap_socket(
  client, server_hostname=SERVER_HOST
)

client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if __name__ == '__main__':
  client.connect((SERVER_HOST, SERVER_PORT))
  
  client.sendall('Hello babyyyyy'.encode('utf-8'))
  
  client.close()