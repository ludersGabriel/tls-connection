import os

from clientClass import Client
from message import Message, MessageTypes

class Interface:
  client = None
  
  def __init__(self, client):
    assert isinstance(client, Client)
    
    self.client = client
    print('Interface created')
    
  def help(self):
    print(
      '''
        Commands:
        - getAllTrainers: get all trainers
        - getTrainer <id>: get a trainer
        - createTrainer <name> <age> <hometown>: create a trainer
        - updateTrainer <id> <name> <age> <hometown>: update a trainer
        - deleteTrainer <id>: delete a trainer
        - exit: exit the program
      '''
    )
    
  def getAllTrainers(self):
    message = Message('getAllTrainers', MessageTypes.trainer)
    
    self.client.send(message)
    
    return message
    
  def readCommand(self):
    while True:
      data = input('>>> ').split(' ')
  
      if data[0] == 'getAllTrainers':
        return self.getAllTrainers()
      # elif data[0] == 'getTrainer':
      #   self.getTrainer(data[1])
      # elif data[0] == 'createTrainer':
      #   self.createTrainer(data[1], data[2], data[3])
      # elif data[0] == 'updateTrainer':
      #   self.updateTrainer(data[1], data[2], data[3], data[4])
      # elif data[0] == 'deleteTrainer':
      #   self.deleteTrainer(data[1])
      elif data[0] == 'exit':
        self.client.close()
        os._exit(0)
      elif data[0] == 'help':
        self.help()
      else:
        print('Invalid command. Type "help" to see the commands.')