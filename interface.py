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
    print(f' {colors.OKBLUE} - createTrainer{colors.ENDC}: create a trainer')
    print(f' {colors.OKBLUE} - updateTrainer <id>{colors.ENDC}: update a trainer')
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
  
  def readInput(self):
    name = input('Name: ').replace(' ', '_')
    name = ''.join([i for i in name if not i.isdigit()])
    
    while name == '':
      print("Name can't be empty and has to be string")
      name = input('Name: ').replace(' ', '_')
      name = ''.join([i for i in name if not i.isdigit()])
    
    age = input('Age: ')
    while isinstance(age, int) == False:
      try:
        age = int(age)
      except:
        print("Age must be a number")
        age = input('Age: ')
        
    hometown = input('Hometown: ').replace(' ', '_')
    hometown = ''.join([i for i in hometown if not i.isdigit()])
    
    while hometown == '':
      print("Hometown can't be empty and has to be string")
      hometown = input('Hometown: ').replace(' ', '_')
      hometown = ''.join([i for i in hometown if not i.isdigit()])
      
    return name, age, hometown
  
  def createTrainer(self):
    
    name, age, hometown = self.readInput()
    
    message = Message(f'createTrainer {name} {age} {hometown}', MessageTypes.trainer)
    
    self.client.send(message)
    
    return message
  
  def readUpdateInput(self):
    name = input('Name: ').replace(' ', '_')
    if name != '':
      name = ''.join([i for i in name if not i.isdigit()])
      while name == '':
        print("Name can't be empty and has to be string")
        name = input('Name: ').replace(' ', '_')

        if name == '':
          break
        name = ''.join([i for i in name if not i.isdigit()])

    age = input('Age: ')
    while isinstance(age, int) == False and age != '':
      try:
        age = int(age)
      except:
        print("Age must be a number")
        age = input('Age: ')
    
    hometown = input('Hometown: ').replace(' ', '_')
    if hometown != '':
      hometown = ''.join([i for i in hometown if not i.isdigit()])
      while hometown == '':
        print("Hometown can't be empty and has to be string")
        hometown = input('Hometown: ').replace(' ', '_')

        if hometown == '':
          break
        hometown = ''.join([i for i in hometown if not i.isdigit()])
    
    return name, age, hometown
  
  def updateTrainer(self, id):
    print("Just hit enter if you dont want to update a field")
    
    name, age, hometown = self.readUpdateInput()

    if name == '':
      name = 'null'
    if age == '':
      age = 'null'
    if hometown == '':
      hometown = 'null'
    
    message = Message(f'updateTrainer {id} {name} {age} {hometown}', MessageTypes.trainer)
    
    self.client.send(message)
    
    return message
  
  def deleteTrainer(self, id):
    message = Message(f'deleteTrainer {id}', MessageTypes.trainer)
    
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
        return self.createTrainer()
      elif data[0] == 'updateTrainer':
        return self.updateTrainer(data[1])
      elif data[0] == 'deleteTrainer':
        return self.deleteTrainer(data[1])
      elif data[0] == 'exit':
        self.client.close()
        os._exit(0)
      elif data[0] == 'help':
        self.help()
      else:
        print('Invalid command. Type "help" to see the commands.')