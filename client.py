import sys
from clientClass import Client
from interface import Interface

if __name__ == '__main__':
  withMan = False
  
  if len(sys.argv) > 2:
    print('Usage: python3 client.py [man]')
    exit(1)
    
  if len(sys.argv) == 2:
    withMan = True
  
  # Creates a client and interface instances
  client = Client(withMan)
  interface = Interface(client)
  
  
  # Client creates a SSL socket
  client.sslConnect()
  
  connected = True
  interface.help()
  
  while connected:
    
    # Read command and handle response
    sent = interface.readCommand()
    client.handleResp(sent)
    
  # Closes client instance
  client.close()