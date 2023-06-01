import socket, ssl

HOST = '127.0.0.1'
PORT = 8080

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

context.load_verify_locations('certificate.crt')
context.load_cert_chain(certfile='certificate.crt', keyfile='server.key')
context.check_hostname = False

if __name__ == '__main__':
  print(context)
  
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  
  server.bind((HOST, PORT))
  
  server.listen(10)
  
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

      