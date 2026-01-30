from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database as MongoDatabase
from pymongo.errors import CollectionInvalid

from app.core.config import config
from .github_model import GitHub

class Database:
  github_collection: Collection[GitHub]

  def __init__(self, host: str, port: int):
    client = MongoClient(host=host, port=port, )
    db: MongoDatabase = client["github_database"]
    try:
      db.create_collection(
        "github",
        timeseries={
          "timeField": "timestamp",
        }
      )
    except CollectionInvalid:
      pass
    self.github_collection = db["github"]

# singleton instance for mongodb database client for collection name 'github' under database name 'github_database'
db = Database(host=config.database_host, port=config.database_port).github_collection