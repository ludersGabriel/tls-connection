import redis
from redis.commands.json.path import Path
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
import redis.commands.search.field as fields
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query

schema = (
    fields.NumericField("$.id", as_name="id"),
    fields.TextField("$.name", as_name="name"), 
    fields.VectorField("$.type", as_name="type")
)

class Db:
  db = None
  indexedDb = None
  
  def __init__(self):
    self.db = redis.Redis(
      host='localhost',
      port=6379,
      decode_responses=True
    )
    
    self.indexedDb = self.db.ft("idx:pokemon")
    
    self.indexedDb.create_index(
      schema,
      definition=IndexDefinition(prefix=['pokemon:'], index_type=IndexType.JSON)
    )
    
    print('Db created')
    

if __name__ == '__main__':
  db = Db()
