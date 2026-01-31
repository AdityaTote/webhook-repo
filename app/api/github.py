from flask import Blueprint, request

from app.services.github import GithubService

github = Blueprint("Github", __name__, url_prefix="/github")

@github.route("/events", methods=["GET"])
def get_github_data():
  since = request.args.get('since')
  data = GithubService.git_github_data(since)
  return {
    "data": data
  }, 200