from server import server
from clientClass import Client

if __name__ == '__main__':
  client = Client(server)
  client.sslConnect()
  
  client.send('Hello babyyyyy')
  
  client.close()