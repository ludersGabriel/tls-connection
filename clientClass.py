import ssl, socket, os
from dotenv import load_dotenv

class Client:
  clientCert = None
  clientKey = None
  serverCert = None
  serverCommonName = None
  serverHost = None
  serverPort = None
  
  context = None
  client = None
  
  def __init__(self):
    self.readEnv()
    self.createContext()
    
    
    print('Client created')
    
  def createContext(self):
    self.context = ssl.create_default_context(
      ssl.Purpose.SERVER_AUTH,
      cafile=self.serverCert
    )
    self.context.load_cert_chain(
      certfile=self.clientCert, keyfile=self.clientKey
    )
    
    self.client = socket.socket(
      socket.AF_INET, socket.SOCK_STREAM
    )
    
    assert isinstance(self.client, socket.socket)
    assert isinstance(self.context, ssl.SSLContext)
  
  def readEnv(self):
    load_dotenv()
    
    self.clientCert = os.getenv('CLIENT_CERT')
    self.clientKey = os.getenv('CLIENT_KEY')
    self.serverCert = os.getenv('SERVER_CERT')
    self.serverCommonName = os.getenv('COMMON_NAME')
    self.serverPort = int(os.getenv('PORT'))
    self.serverHost = os.getenv('HOST')
    
  def sslConnect(self):
    self.client = self.context.wrap_socket(
      self.client,
      server_side=False,
      server_hostname=self.serverCommonName
    )
    
    self.client.connect(
      (self.serverHost, self.serverPort)
    )
    
  def send(self, message):
    self.client.send(message.encode('utf-8'))
    
  def close(self):
    self.client.close()
  
    
  