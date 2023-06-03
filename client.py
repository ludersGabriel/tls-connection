from clientClass import Client
from interface import Interface

if __name__ == '__main__':
  client = Client()
  interface = Interface(client)
  
  client.sslConnect()
  
  connected = True
  interface.help()
  
  while connected:
    
    sent = interface.readCommand()
  
    client.handleResp(sent)
    
  client.close()