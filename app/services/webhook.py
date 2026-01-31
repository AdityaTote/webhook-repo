from app.database.github_model import Action, GitHub
from app.schema.webhook import PullRequestWebhookPayload, WebhookPayload
from app.database.database import db

class WebhookService:
  @staticmethod
  def store_data(data: WebhookPayload | PullRequestWebhookPayload, action: Action):
    if action == Action.push:
      if isinstance(data, WebhookPayload) and data.head_commit is not None and data.head_commit.author.name is not None:
        db.insert_one(GitHub(
          action=action.value, # type:ignore
          request_id=data.head_commit.id,
          author=data.head_commit.author.name,
          from_branch=data.ref.replace("refs/heads/", ""),
          to_branch=data.ref.replace("refs/heads/", ""),
          timestamp=data.head_commit.timestamp
        ))
    elif action == Action.pull_request:
      if isinstance(data, PullRequestWebhookPayload) and data.sender.login is not None:
        db.insert_one(GitHub(
          action=action.value, # type:ignore
          request_id=str(data.pull_request.id),
          author=data.sender.login,
          from_branch=data.pull_request.head.ref,
          to_branch=data.pull_request.base.ref,
          timestamp=data.pull_request.created_at
        ))
    elif action == Action.merge:
      if isinstance(data, PullRequestWebhookPayload) and data.sender.login is not None:
        merge_timestamp = data.pull_request.merged_at or data.pull_request.updated_at
        db.insert_one(GitHub(
          action=action.value, # type:ignore
          request_id=str(data.pull_request.id),
          author=data.sender.login,
          from_branch=data.pull_request.head.ref,
          to_branch=data.pull_request.base.ref,
          timestamp=merge_timestamp
        ))
    return True