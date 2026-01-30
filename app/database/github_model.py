from enum import Enum
from typing import TypedDict

class Action(Enum):
  push = "PUSH"
  pull_request = "PULL_REQUEST"
  merge = "MERGE"

class GitHub(TypedDict):
  request_id: str
  author: str
  action: Action
  from_branch: str
  to_branch: str
  timestamp: str