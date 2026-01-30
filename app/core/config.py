import os
from dotenv import load_dotenv

load_dotenv()

class Config:
  port: int = int(os.getenv("PORT", ""))
  database_host:str =  os.getenv("DATABASE_HOST", "")
  database_port:int =  int(os.getenv("DATABASE_PORT", ""))
  redis_host:str =  os.getenv("REDIS_HOST", "")
  redis_port:int =  int(os.getenv("REDIS_PORT", ""))
  github_secret:str =  os.getenv("GITHUB_SECRET", "")

config = Config()