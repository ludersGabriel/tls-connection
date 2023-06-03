import ssl, socket, os, pickle 
from dotenv import load_dotenv

from db import Db
from message import Message, MessageTypes
from logger import Logger, LoggerTypes

class Server:
  host = None
  port = None
  commonName = None
  serverCert = None
  serverKey = None
  clientCert = None
  logsPath = None
  
  MAX_TCP_SIZE = 2 ** 16 - 1
  
  db = None  
  context = None
  sock = None  
  logger = None
   
  def __init__(self):
    self.readEnv()
    self.createContext()

    self.db = Db()
    
    self.logger = Logger(self.logsPath)
    
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
    self.logsPath = os.getenv('SERVER_LOG')
  
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
        self.logger.logMessage(
          'Connected by ' + str(client_addr),
          LoggerTypes.INFO
        )
        
        while True:
          data = connection.recv(self.MAX_TCP_SIZE)
          
          if not data:
            self.logger.logMessage(
              'Connection closed by ' + str(client_addr),
              LoggerTypes.INFO
            )
            break
          
          data = pickle.loads(data)
          
          assert isinstance(data, Message)
          
          resp, type = self.handleMessage(data)              

          Logger.logMessage(self.logger, resp, type)
          
          packet = pickle.dumps(resp)
          
          if len(packet) > self.MAX_TCP_SIZE:
            self.logger.logMessage(
              f'Packet too large: {len(packet)} bytes', LoggerTypes.ERROR
            )
            raise Exception('Packet too large')
          
          connection.sendall(packet)

  def handleTrainer(self, message):
    assert isinstance(message, Message)
    assert isinstance(message.data, str)
    
    operation = message.data.split(' ')[0]
    
    data = None
    loggerType = LoggerTypes.INFO
    
    if operation == 'getAllTrainers':
      data = self.db.trainer.findAll()
    else:
      data = 'Invalid operation or no data found'
      loggerType = LoggerTypes.ERROR
      
    return Message(data, MessageTypes.trainer), loggerType
    
  def handleMessage(self, message):
    assert isinstance(message, Message)
    
    if(message.messageType == MessageTypes.trainer):
      return self.handleTrainer(message)