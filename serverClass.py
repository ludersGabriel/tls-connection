import ssl, socket

class Server:
  host = '127.0.0.1'
  port = 8080
  commonName = 'astora'
  serverCert = './server/server.crt'
  serverKey = './server/server.key'
  clientCert = './client/client.crt'
  
  context = None
  sock = None  
  
  def __init__(self):
    self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    self.context.verify_mode = ssl.CERT_REQUIRED
    self.context.load_cert_chain(certfile=self.serverCert, keyfile=self.serverKey)
    self.context.load_verify_locations(cafile=self.clientCert)
    
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    assert isinstance(self.sock, socket.socket)
    assert isinstance(self.context, ssl.SSLContext)

    print('Server created')
  
  def sslBind(self):
    self.sock.bind((self.host, self.port))  
    self.sock.listen(5)
    
    self.sock = self.context.wrap_socket(
      self.sock, server_side=True
    )
    
  def listen(self):
    while True:
      connection, client_addr = self.sock.accept()
      
      with connection:
        print('Connected by', client_addr)
        
        while True:
          data = connection.recv(1024)
          
          if not data:
            break
          
          print(f'received: {data.decode("utf-8")}')
          
        connection.close()