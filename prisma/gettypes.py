import json

# Load pokemons and trainers in JSON
with open('seed.json') as f: 
  data = json.load(f)
  
  types = [] 
  
  # For each pokemon, get its Types
  for pokemon in data["pokemons"]:
    for type in pokemon["type"]:
      # If it is a new Type, add it to the list
      if type not in types:
        types.append(type)
        
  for type in types:
    print(type)