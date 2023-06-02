from serverClass import Server
import ssl, socket

class Client:
  clientCert = './client/client.crt'
  clientKey = './client/client.key'
  
  context = None
  server = None
  client = None
  
  def __init__(self, server):
    assert isinstance(server, Server) 
    self.server = server
    
    self.context = ssl.create_default_context(
      ssl.Purpose.SERVER_AUTH,
      cafile=self.server.serverCert
    )
    self.context.load_cert_chain(
      certfile=self.clientCert, keyfile=self.clientKey
    )
    
    self.client = socket.socket(
      socket.AF_INET, socket.SOCK_STREAM
    )
    
    assert isinstance(self.client, socket.socket)
    assert isinstance(self.context, ssl.SSLContext)
    
    print('Client created')
    
  def sslConnect(self):
    self.client = self.context.wrap_socket(
      self.client,
      server_side=False,
      server_hostname=self.server.commonName
    )
    
    self.client.connect(
      (self.server.host, self.server.port)
    )
    
  def send(self, message):
    self.client.send(message.encode('utf-8'))
    
  def close(self):
    self.client.close()
  
    
  