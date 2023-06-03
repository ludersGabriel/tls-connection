import json

with open('seed.json') as f: 
  data = json.load(f)
  
  types = [] 
  
  for pokemon in data["pokemons"]:
    for type in pokemon["type"]:
      if type not in types:
        types.append(type)
        
  for type in types:
    print(type)