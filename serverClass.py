import ssl, socket, os
from dotenv import load_dotenv

from db import Db
class Server:
  host = None
  port = None
  commonName = None
  serverCert = None
  serverKey = None
  clientCert = None
  
  db = None  
  context = None
  sock = None  
  
  def __init__(self):
    self.readEnv()
    self.createContext()

    db = Db()
    
    print('Server created')
  
  def createContext(self):
    self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    self.context.verify_mode = ssl.CERT_REQUIRED
    self.context.load_cert_chain(certfile=self.serverCert, keyfile=self.serverKey)
    self.context.load_verify_locations(cafile=self.clientCert)
    
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    assert isinstance(self.sock, socket.socket)
    assert isinstance(self.context, ssl.SSLContext)
  
  def readEnv(self):
    load_dotenv()
    
    self.host = os.getenv('HOST')
    self.port = int(os.getenv('PORT'))
    self.commonName = os.getenv('COMMON_NAME')
    self.serverCert = os.getenv('SERVER_CERT')
    self.serverKey = os.getenv('SERVER_KEY')
    self.clientCert = os.getenv('CLIENT_CERT')
  
  def sslBind(self):
    self.sock.bind((self.host, self.port))  
    self.sock.listen(5)
    
    self.sock = self.context.wrap_socket(
      self.sock, server_side=True
    )
    
  def listen(self):
    while True:
      connection = None 
      client_addr = None 
      
      while connection is None:
        try:
          connection, client_addr = self.sock.accept()
        except Exception as e:
          # write a logger that will log these errors to a file
          print(e)
      
      with connection:
        print('Connected by', client_addr)
        
        while True:
          data = connection.recv(1024)
          
          if not data:
            break
          
          print(f'received: {data.decode("utf-8")}')
          
        connection.close()