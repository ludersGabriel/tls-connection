from clientClass import Client
from interface import Interface

if __name__ == '__main__':
  # Creates a client and interface instances
  client = Client()
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