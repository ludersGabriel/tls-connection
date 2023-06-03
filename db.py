from prisma import Prisma
from trainer import Trainer

class Db:
  prisma = None
  trainer = None
  
  def __init__(self):
    self.prisma = Prisma()
    self.prisma.connect()
    
    self.trainer = Trainer(self.prisma)
    print('Db created')
   
  def disconnect(self):
    self.prisma.disconnect()
    print('Db disconnected')

if __name__ == '__main__':
  db = Db()
  
  trainers = db.trainer.findAll()
  
  for trainer in trainers:
    print(f'{trainer.name} from {trainer.hometown}')
  
  db.disconnect()