from prisma import Prisma
from trainer import Trainer

class Db:
  prisma = None
  trainer = None
  
  def __init__(self):
    # Connect to the database
    self.prisma = Prisma()
    self.prisma.connect()
    
    # Creates an instance of trainer
    self.trainer = Trainer(self.prisma)
    print('Db created')
   
  # Disconnects of the database
  def disconnect(self):
    self.prisma.disconnect()
    print('Db disconnected')

if __name__ == '__main__':
  db = Db()
  
  trainers = db.trainer.findAll()
  
  for trainer in trainers:
    print(f'{trainer.name} from {trainer.hometown}')
  
  db.disconnect()