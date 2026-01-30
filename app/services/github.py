from bson import ObjectId
from app.database.database import db

class GithubService():
  @staticmethod
  async def git_github_data(since: str | None):
    data = []
    
    try:
      if since is None:
        data = list(db.find().sort("_id", -1).limit(50))
      else:
        data = list(db.find({
          "_id": {"$gt": ObjectId(since)}
        }).sort("_id", 1))
      
      for item in data:
        if '_id' in item:
          item['_id'] = str(item['_id'])

    except Exception as e:
      print(f"MongoDB error: {e}")
      data = []

    return data