
import enum

class MessageTypes(enum.Enum):
  hello = 1
  trainer = 2
  pokemon = 3

class Message:
  data = None
  messageType = None
  
  def __init__(self, data, type):
    assert isinstance(type, MessageTypes)
    
    self.data = data
    self.messageType = type
  