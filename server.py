import socket, ssl

HOST = '127.0.0.1'
PORT = 8080
SERVER_COMMON_NAME = 'astora'
SERVER_CERT = './server/server.crt'
SERVER_KEY = './server/server.key'
CLIENT_CERT = './client/client.crt'

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
context.load_verify_locations(cafile=CLIENT_CERT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if __name__ == '__main__':
  server.bind((HOST, PORT))  
  server.listen(5)
  
  server = context.wrap_socket(
    server, server_side=True
  )
  
  while True:
    connection, client_addr = server.accept()
    
    with connection:
      print('Connected by', client_addr)
      
      while True:
        data = connection.recv(1024)
        
        if not data:
          break
        
        print(f'received: {data.decode("utf-8")}')
        
      connection.close()

      