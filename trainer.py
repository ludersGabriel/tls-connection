from prisma import Prisma

class Trainer:
  prisma = None
  
  # Instantiates prisma in the trainer class
  def __init__(self, prisma):
    assert isinstance(prisma, Prisma)
    
    self.prisma = prisma

  # Find all trainers in the database
  def findAll(self):
    return self.prisma.trainer.find_many()
  
  # Find one trainer in the database
  def findOne(self, id):
    return self.prisma.trainer.find_unique(
      where={
        'id': id
      }
    )
  
  # Creates a new trainer in the database
  def create(self, data):
    return self.prisma.trainer.create(
      {
        'age': data['age'],
        'name': data['name'],
        'hometown': data['hometown']
      }
    )
    
  # Updates an existing trainer in the database
  def update(self, id, data):
    return self.prisma.trainer.update(
      where = {
        'id': id
      },
      data = data
    )
    
  # Deletes an existing trainer in the database
  def delete(self, id):
    return self.prisma.trainer.delete(
      where = {
        'id': id
      }
    )