from clientClass import Client

if __name__ == '__main__':
  client = Client()
  client.sslConnect()
  
  client.send('Hello babyyyyy')
  
  client.close()