import redis
import json
from redis.commands.json.path import Path


db = redis.Redis(
  host='localhost',
  port=6379,
  decode_responses=True
)

db.flushall()

with open('treated.txt') as f: 
  data = json.load(f)
  
  for i in data:
    db.json().set(f'pokemon:{i["id"]}', Path.root_path(), i)