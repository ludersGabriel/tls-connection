import socket, ssl

HOST='127.0.0.1'
PORT=8000
SERVER_CERT='server.crt'
SERVER_KEY='server.key'
CLIENT_CERT='client.crt'
COMMON_NAME='astora'

if __name__ == '__main__':
  sock = socket.create_server((HOST, PORT))
  
  context = ssl.create_default_context(
    ssl.Purpose.CLIENT_AUTH
  )
  context.verify_mode = ssl.CERT_REQUIRED
  context.load_cert_chain(
    certfile=SERVER_CERT,
    keyfile=SERVER_KEY
  )
  context.load_verify_locations(
    cafile=CLIENT_CERT
  )
  
  sock = context.wrap_socket(
    sock, server_side=True
  )
  
  conn, adrr = sock.accept()
  
  print(conn.recv())
  
  
  