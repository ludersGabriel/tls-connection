from prisma import Prisma
import json

def main(): 
  prisma = Prisma()
  prisma.connect()
  
  prisma.execute_raw('DELETE FROM "public"."Trainer" CASCADE')
  prisma.execute_raw('DELETE FROM "public"."Pokemon" CASCADE')
  
  with open("seed.json") as f: 
    data = json.load(f)
    for trainer in data['trainers']:
      prisma.trainer.create({
        'name': trainer['name'],
        'age': trainer['age'],
        'hometown': trainer['hometown']
      })
    
    for pokemon in data['pokemons']:
      listType = []
      for type in pokemon['type']:
        listType.append(type)
      
      prisma.pokemon.create({
        'name': pokemon['name'],
        'type': listType
      })  
      
  prisma.disconnect()
  
if __name__ == '__main__':
  main()