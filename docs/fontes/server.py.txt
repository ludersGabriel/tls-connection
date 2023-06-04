from serverClass import Server

# Creates a Server instance
server = Server()

if __name__ == '__main__':
  server.sslBind()
  server.listen()

      