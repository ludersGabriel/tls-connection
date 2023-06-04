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

  # Prints help menu in the IO stream  
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
    
    
  # Creates a message object to get all trainers and sends it
  def getAllTrainers(self):
    message = Message('getAllTrainers', MessageTypes.trainer)
    
    self.client.send(message)
    
    return message
    
  # Creates a message object to get a trainer and sends it
  def getTrainer(self, id):
    message = Message(f'getTrainer {id}', MessageTypes.trainer)
    
    self.client.send(message)
    
    return message
  
  # Reads the input to create a trainer
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
    
    # Reads and treats the user input to create a trainer
    name, age, hometown = self.readInput()
    
    # Creates a message object
    message = Message(f'createTrainer {name} {age} {hometown}', MessageTypes.trainer)


    # Sends the packet
    self.client.send(message)
    
    return message
  
  # Reads the input to update a trainer
  def readUpdateInput(self):
    # Replaces ' ' to _ so the server knows it is part of a name and not a command
    name = input('Name: ').replace(' ', '_')
    # If name is not empty, it means the Client demands to change the name
    if name != '':
      # Verify if there are'nt any digits in the string
      name = ''.join([i for i in name if not i.isdigit()])
      # If is empty now, the client typed an invalid string
      while name == '':
        print("Name can't be empty and has to be string")
        name = input('Name: ').replace(' ', '_')

        if name == '':
          break
        name = ''.join([i for i in name if not i.isdigit()])

    # Reads and treats Age of trainer
    age = input('Age: ')
    while isinstance(age, int) == False and age != '':
      try:
        age = int(age)
      except:
        print("Age must be a number")
        age = input('Age: ')
    
    # Reads and treats Hometown of trainer
    # Replaces ' ' to _ so the server knows it is part of a name and not a command
    hometown = input('Hometown: ').replace(' ', '_')
    # If name is not empty, it means the Client demands to change the hometown
    if hometown != '':
      # Remove the digits
      hometown = ''.join([i for i in hometown if not i.isdigit()])
      # If is empty now, the client typed an invalid string
      while hometown == '':
        print("Hometown can't be empty and has to be string")
        hometown = input('Hometown: ').replace(' ', '_')

        if hometown == '':
          break
        hometown = ''.join([i for i in hometown if not i.isdigit()])
    
    return name, age, hometown
  
  # Creates a message object to update a trainer and sends it
  def updateTrainer(self, id):
    print("Just hit enter if you dont want to update a field")
    
    # Reads and treats the user input to update a trainer
    name, age, hometown = self.readUpdateInput()

    if name == '':
      name = 'null'
    if age == '':
      age = 'null'
    if hometown == '':
      hometown = 'null'
    
    # Creates a message objetc
    message = Message(f'updateTrainer {id} {name} {age} {hometown}', MessageTypes.trainer)
    
    # Sends the packet
    self.client.send(message)
    
    return message
  
  # Creates a message object to delete a trainer and sends it
  def deleteTrainer(self, id):
    message = Message(f'deleteTrainer {id}', MessageTypes.trainer)
    
    self.client.send(message)
    
    return message
  
  def readCommand(self):
    while True:
      data = input('>>> ').split(' ')
  
      # Checks which command the client choose
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