import ssl, socket, os, pickle 
from dotenv import load_dotenv

from db import Db
from message import Message, MessageTypes
from logger import Logger, LoggerTypes

class Server:
  # Client variables
  host = None
  port = None
  commonName = None
  serverCert = None
  serverKey = None
  clientCert = None
  logsPath = None
  
  # Maximum size of TCP packets
  MAX_TCP_SIZE = 2 ** 16 - 1024
  
  db = None  
  context = None
  sock = None  
  logger = None
   
  def __init__(self):
    # Load environment variables and creates a Server context
    self.readEnv()
    self.createContext()

    # Creates an instance of the database
    self.db = Db()
    
    # Creates an instance of the logger
    self.logger = Logger(self.logsPath)
    
    print('Server created')
  
    # Creates a SSL server context
  def createContext(self):
    self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    self.context.verify_mode = ssl.CERT_REQUIRED
    self.context.load_cert_chain(certfile=self.serverCert, keyfile=self.serverKey)
    self.context.load_verify_locations(cafile=self.clientCert)
    
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    assert isinstance(self.sock, socket.socket)
    assert isinstance(self.context, ssl.SSLContext)
  
  # Load environment variables
  def readEnv(self):
    load_dotenv()
    
    self.host = os.getenv('HOST')
    self.port = int(os.getenv('PORT'))
    self.commonName = os.getenv('COMMON_NAME')
    self.serverCert = os.getenv('SERVER_CERT')
    self.serverKey = os.getenv('SERVER_KEY')
    self.clientCert = os.getenv('CLIENT_CERT')
    self.logsPath = os.getenv('SERVER_LOG')
  
  # Binds the socket to a port of the system and listens
  def sslBind(self):
    self.sock.bind((self.host, self.port))  
    self.sock.listen(5)
    
    # Wraps the socket with TLS
    self.sock = self.context.wrap_socket(
      self.sock, server_side=True
    )
    
  def listen(self):
    while True:
      connection = None 
      client_addr = None 
      
      # Keeps listening till it finds a connection
      while connection is None:
        try:
          connection, client_addr = self.sock.accept()
        except Exception as e:
          self.logger.logMessage(
            'Error accepting connection: ' + str(e),
            LoggerTypes.ERROR
          )
          continue
      
      # When it finds a connection, writes into the log file
      with connection:
        self.logger.logMessage(
          'Connected by ' + str(client_addr),
          LoggerTypes.INFO
        )
        
        while True:
          # Receives message from client
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

          # Sends response to client
          self.sendResp(resp, connection, type)

  def sendResp(self, message, connection, type):
    # Verify that the instances were created properly
    assert isinstance(message, Message)
    assert isinstance(connection, ssl.SSLSocket)
    
    Logger.logMessage(self.logger, message, type)
          
    packet = pickle.dumps(message)
    
    # Checks if packet have the correct size
    if len(packet) > self.MAX_TCP_SIZE:
      self.logger.logMessage(
        f'Packet too large: {len(packet)} bytes', LoggerTypes.ERROR
      )
      raise Exception('Packet too large')
    
    # sends the packet through the network
    connection.sendall(packet)

  def handleTrainer(self, message):
    # Verify if the message is a Message object or a string
    assert isinstance(message, Message)
    assert isinstance(message.data, str)
    
    # Splits the commands and arguments of the message
    operation = message.data.split(' ')[0]
    split = message.data.split(' ')
    
    data = None
    loggerType = LoggerTypes.INFO
    
    # Treats client operation with the trainer class
    if operation == 'getAllTrainers':
      data = self.db.trainer.findAll()
    elif operation == 'getTrainer':
      data = self.db.trainer.findOne(int(split[1]))
    elif operation == 'createTrainer':
      data = self.db.trainer.create(
        {
          'name': split[1].replace('_', ' '),
          'age': int(split[2]),
          'hometown': split[3].replace('_', ' ')
        }
      )
    elif operation == 'updateTrainer':
      dbData = self.db.trainer.findOne(int(split[1]))
      
      if dbData is None:
        data = None
        loggerType = LoggerTypes.ERROR
      else:
        name = split[2] if split[2] != 'null' else dbData.name
        age = int(split[3]) if split[3] != 'null' else dbData.age
        hometown = split[4] if split[4] != 'null' else dbData.hometown
        
        print(name, age, hometown)
        
        # Calls the update function of db class
        data = self.db.trainer.update(
          int(split[1]),
          {
            'name': name.replace('_', ' '),
            'age': age,
            'hometown': hometown.replace('_', ' ')
          }
        )
    
    elif operation == 'deleteTrainer':
      # calls the delete function of db class
      data = self.db.trainer.delete(int(split[1]))
      
      if data == None:
        loggerType = LoggerTypes.ERROR
      else:
        loggerType = LoggerTypes.INFO
      
    else:
      data = 'Invalid operation or no data found'
      loggerType = LoggerTypes.ERROR
      
    return Message(data, MessageTypes.trainer), loggerType
    
  def handleMessage(self, message):
    assert isinstance(message, Message)
    
    if(message.messageType == MessageTypes.trainer):
      return self.handleTrainer(message)