import os

from clientClass import Client
from message import Message, MessageTypes
from logger import colors

class Interface:
  client = None
  
  def __init__(self, client):
    assert isinstance(client, Client)
    
    self.client = client
    print('Interface created')
    
  def help(self):
    print(colors.OKGREEN + '\nCommands')
    print('--------')
    
    print(f' {colors.OKBLUE} - getAllTrainers{colors.ENDC}: get all trainers')
    print(f' {colors.OKBLUE} - getTrainer <id>{colors.ENDC}: get a trainer')
    print(f' {colors.OKBLUE} - createTrainer <name> <age> <hometown>{colors.ENDC}: create a trainer')
    print(f' {colors.OKBLUE} - updateTrainer <id> <name> <age> <hometown>{colors.ENDC}: update a trainer')
    print(f' {colors.OKBLUE} - deleteTrainer <id>{colors.ENDC}: delete a trainer')
    print(f' {colors.OKBLUE} - exit{colors.ENDC}: exit the program')
    print(f' {colors.OKBLUE} - help{colors.ENDC}: shows commands\n')
    
    
  def getAllTrainers(self):
    message = Message('getAllTrainers', MessageTypes.trainer)
    
    self.client.send(message)
    
    return message
    
  def getTrainer(self, id):
    message = Message(f'getTrainer {id}', MessageTypes.trainer)
    
    self.client.send(message)
    
    return message
  
  def createTrainer(self, name, age, hometown):
    message = Message(f'createTrainer {name} {age} {hometown}', MessageTypes.trainer)
    
    self.client.send(message)
    
    return message
  
  def readCommand(self):
    while True:
      data = input('>>> ').split(' ')
  
      if data[0] == 'getAllTrainers':
        return self.getAllTrainers()
      elif data[0] == 'getTrainer':
        return self.getTrainer(data[1])
      elif data[0] == 'createTrainer':
        return self.createTrainer(data[1], data[2], data[3])
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