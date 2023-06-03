import enum, os

from message import Message, MessageTypes

class colors():
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

class LoggerTypes(enum.Enum):
  ERROR = 1
  INFO = 2
  WARNING = 3

class Logger:
  file = None
  
  def __init__(self, path):
    assert isinstance(path, str)
    
    try:
      self.file = open(path, 'w')
    except Exception as e:
      print(e)
      print(colors.FAIL + 'Could not create logger' + colors.ENDC)

      os._exit(1)
    
    print(colors.OKGREEN + 'Logger created' + colors.ENDC)

  def logMessage(self, message, type): 
    assert isinstance(message, Message) or isinstance(message, str)
    assert isinstance(type, LoggerTypes)
  
    log = ''
      
    if(type == LoggerTypes.ERROR):
      log += colors.FAIL + '[ERROR] ' + colors.ENDC
    elif(type == LoggerTypes.INFO):
      log += colors.OKGREEN + '[INFO] ' + colors.ENDC
    else:
      log += colors.WARNING + '[WARNING] ' + colors.ENDC
    
    if isinstance(message, Message):
      log += f'{message.messageType.name}: {message.data}'
    elif isinstance(message, str):
      log += message
    
    print(log)
    
    self.file.write(log + '\n')
    
    self.file.flush()
    