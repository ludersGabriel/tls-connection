import socket, ssl

from server import SERVER_CERT, HOST, PORT, COMMON_NAME

CLIENT_CERT='client.crt'
CLIENT_KEY='client.key'

if __name__ == '__main__':
  sock = socket.create_connection((HOST, PORT))
  
  context = ssl.create_default_context(
    ssl.Purpose.SERVER_AUTH,
    cafile=SERVER_CERT
  )
  context.load_cert_chain(
    certfile=CLIENT_CERT,
    keyfile=CLIENT_KEY
  )
  
  sock = context.wrap_socket(
    sock, 
    server_side=False,
    server_hostname=COMMON_NAME
  )
  
  sock.sendall('Hello, world over TLS!'.encode())