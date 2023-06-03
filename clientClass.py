import ssl, socket, os, pickle
from dotenv import load_dotenv
from message import Message, MessageTypes

from prisma.models import Trainer
from logger import Logger, LoggerTypes

class Client:
  # Client variables
  clientCert = None
  clientKey = None
  serverCert = None
  serverCommonName = None
  serverHost = None
  serverPort = None
  logsPath = None
  
  # Maximum size of TCP packets
  MAX_TCP_SIZE = 2 ** 16 - 1024
      
  context = None
  client = None
  logger = None
  manHost = None
  manPort = None
  
  def __init__(self):
    self.readEnv() # Load environment variables
    self.createContext() # Creates a Client context
    
    self.logger = Logger(self.logsPath)
    
    print('[   OK   ] Client created successfully!')

  # Creates a Client context  
  def createContext(self):
    # Creates a SSL client context
    self.context = ssl.create_default_context(
      ssl.Purpose.SERVER_AUTH,
      cafile=self.serverCert
    )
    # Loads the client certificate
    self.context.load_cert_chain(
      certfile=self.clientCert, keyfile=self.clientKey
    )
    
    # Creates a TCP socket with ipv4
    self.client = socket.socket(
      socket.AF_INET, socket.SOCK_STREAM
    )
    
    # Verify that the instances were created properly
    assert isinstance(self.client, socket.socket)
    assert isinstance(self.context, ssl.SSLContext)
  
  # Load environment variables of .env
  def readEnv(self):
    load_dotenv()
    
    self.clientCert = os.getenv('CLIENT_CERT')
    self.clientKey = os.getenv('CLIENT_KEY')
    self.serverCert = os.getenv('SERVER_CERT')
    self.serverCommonName = os.getenv('COMMON_NAME')
    self.serverPort = int(os.getenv('PORT'))
    self.serverHost = os.getenv('HOST')
    self.logsPath = os.getenv('CLIENT_LOG')
    self.manHost = os.getenv('MAN_HOST')
    self.manPort = int(os.getenv('MAN_PORT'))

  # Wraps the client socket with the SSL  
  def sslConnect(self):
    self.client = self.context.wrap_socket(
      self.client,
      server_side=False,
      server_hostname=self.serverCommonName
    )
    
    # Connects to the server
    self.client.connect(
      (self.serverHost, self.serverPort)
    )
    
  def send(self, message):
    assert isinstance(message, Message)
    
    # Serialize the message object into a byte stream
    packet = pickle.dumps(message)
    
    # Checks if packet have the correct size
    if len(packet) > self.MAX_TCP_SIZE:
      self.logger.logMessage(
        f'Packet too large: {len(packet)} bytes', LoggerTypes.ERROR
      )
      raise Exception('Packet too large')
    
    self.logger.logMessage(
      message, LoggerTypes.INFO
    )
    
    self.client.sendall(packet)
    
  def close(self):
    self.client.close()
  
  def handleGetAllTrainers(self, resp, log):
    log += '\n\nTrainers\n'
    log += '--------\n\n'
    
    for trainer in resp.data:
      assert isinstance(trainer, Trainer)
      
      log += f'{trainer.name}: id {trainer.id}, age {trainer.age} and hometown {trainer.hometown}\n'
      
    self.logger.logMessage(log + '\n', LoggerTypes.INFO)
  
  def handleGetTrainer(self, resp, log):
    if resp.data == None:
      log += 'Trainer not found\n'
      self.logger.logMessage(log, LoggerTypes.WARNING)
      return
    
    assert isinstance(resp.data, Trainer)
    
    log += f'{resp.data.name}: id {resp.data.id}, age {resp.data.age} and hometown {resp.data.hometown}\n'
    
    self.logger.logMessage(log, LoggerTypes.INFO)
  
  def handleCreateTrainer(self, resp, log):
    assert isinstance(resp.data, Trainer)
    
    log += f'created = {resp.data.name}: id {resp.data.id}, age {resp.data.age} and hometown {resp.data.hometown}\n'

    self.logger.logMessage(log, LoggerTypes.INFO)
    
  def handleUpdateTrainer(self, resp, log):
    if resp.data == None:
      log += 'Trainer not found\n'
      self.logger.logMessage(log, LoggerTypes.WARNING)
      return
    
    assert isinstance(resp.data, Trainer)
    
    log += f'updated = {resp.data.name}: id {resp.data.id}, age {resp.data.age} and hometown {resp.data.hometown}\n'

    self.logger.logMessage(log, LoggerTypes.INFO)
    
  def handleDeleteTrainer(self, resp, log):
    if resp.data == None:
      log += 'Trainer not found\n'
      self.logger.logMessage(log, LoggerTypes.WARNING)
      return
    
    assert isinstance(resp.data, Trainer)
    
    log += f'deleted = {resp.data.name}: id {resp.data.id}, age {resp.data.age} and hometown {resp.data.hometown}\n'

    self.logger.logMessage(log, LoggerTypes.INFO)
    
  def handleResp(self, sent): 
    assert isinstance(sent, Message)
    
    r = self.client.recv(self.MAX_TCP_SIZE)
    
    if not r:
      self.looger.logMessage(
        'No response from server', 
        LoggerTypes.ERROR
      )
      return
    
    resp = pickle.loads(r)
    assert isinstance(resp, Message)
    
    log = ''
    
    sentSplit = sent.data.split(' ')

    op = f'operation and params: {sentSplit}'
    self.logger.logMessage(op, LoggerTypes.INFO)
    
    if sentSplit[0] == 'getAllTrainers':
      self.handleGetAllTrainers(resp, log)
    elif sentSplit[0] == 'getTrainer':
      self.handleGetTrainer(resp, log)
    elif sentSplit[0] == 'createTrainer':
      self.handleCreateTrainer(resp, log)
    elif sentSplit[0] == 'updateTrainer':
      self.handleUpdateTrainer(resp, log)
    elif sentSplit[0] == 'deleteTrainer':
      self.handleDeleteTrainer(resp, log)

  