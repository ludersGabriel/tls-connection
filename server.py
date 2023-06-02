from serverClass import Server

server = Server()

if __name__ == '__main__':
  server.sslBind()
  server.listen()

      