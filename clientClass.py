import ssl, socket, os, pickle
from dotenv import load_dotenv
from message import Message, MessageTypes

from prisma.models import Trainer
from logger import Logger, LoggerTypes

class Client:
  clientCert = None
  clientKey = None
  serverCert = None
  serverCommonName = None
  serverHost = None
  serverPort = None
  logsPath = None
      
  context = None
  client = None
  logger = None
  
  def __init__(self):
    self.readEnv()
    self.createContext()
    
    self.logger = Logger(self.logsPath)
    
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
    self.logsPath = os.getenv('CLIENT_LOG')
    
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
    assert isinstance(message, Message)
    
    self.client.sendall(pickle.dumps(message))
    
  def close(self):
    self.client.close()
  
  
  def handleResp(self, sent): 
    assert isinstance(sent, Message)
    
    resp = pickle.loads(self.client.recv(1024))
    assert isinstance(resp, Message)
    
    log = ''
    
    if sent.data.split(' ')[0] == 'getAllTrainers':
      log += '\n\nTrainers\n'
      log += '--------\n\n'
      
      for trainer in resp.data:
        assert isinstance(trainer, Trainer)
        
        log += f'{trainer.name}: id {trainer.id}, age {trainer.age} and hometown {trainer.hometown}\n'
        
      self.logger.logMessage(log + '\n', LoggerTypes.INFO)

  