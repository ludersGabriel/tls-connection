from prisma import Prisma
import json

def main(): 
  # Connect to the database
  prisma = Prisma()
  prisma.connect()
  
  # Delete old data of the database
  prisma.execute_raw('DELETE FROM "public"."Trainer" CASCADE')
  prisma.execute_raw('DELETE FROM "public"."Pokemon" CASCADE')
  
  # Load pokemons and trainers in JSON
  with open("seed.json") as f: 
    data = json.load(f)
    # Create the trainers in the database
    for trainer in data['trainers']:
      prisma.trainer.create({
        'name': trainer['name'],
        'age': trainer['age'],
        'hometown': trainer['hometown']
      })
    # Create the pokémons in the database
    for pokemon in data['pokemons']:
      listType = []
      for type in pokemon['type']:
        listType.append(type)
      
      prisma.pokemon.create({
        'name': pokemon['name'],
        'type': listType
      })  
      
  # Disconnect from the database
  prisma.disconnect()
  
if __name__ == '__main__':
  main()