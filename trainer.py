from prisma import Prisma

class Trainer:
  prisma = None
  
  def __init__(self, prisma):
    assert isinstance(prisma, Prisma)
    
    self.prisma = prisma

  def findAll(self):
    return self.prisma.trainer.find_many()
  
  def findOne(self, id):
    return self.prisma.trainer.findOne(id)
  
  def create(self, data):
    return self.prisma.trainer.create(
      {
        'age': data['age'],
        'name': data['name'],
        'hometown': data['hometown']
      }
    )
    
  def update(self, id, data):
    return self.prisma.trainer.update(
      where = {
        'id': id
      },
      data = data
    )
    
  def delete(self, id):
    return self.prisma.trainer.delete(
      where = {
        'id': id
      }
    )