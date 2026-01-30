from flask import Blueprint, request
from app.core.utils.validate_headers import validate_webhook
from app.database.github_model import Action
from app.services.webhook import WebhookService
from app.schema.webhook import PullRequestWebhookPayload, WebhookPayload
import json


webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
async def receiver():
    # extract hash signature from header
    sign = request.headers.get("X-Hub-Signature-256")
    if not sign:
        return {}, 409
    
    # validate the signature with the hash of secret
    validate_webhook(request.get_data(), sign)

    # extract action of webhook ('push', 'pull_request')
    action = request.headers.get("X-GitHub-Event")
    if not action:
        return {}, 409
    
    data: bool = False

    try:
        content_type = request.content_type or ""
        if "application/x-www-form-urlencoded" in content_type:
            payload_str = request.form.get('payload', '{}')
            json_data = json.loads(payload_str)
        else:
            json_data = request.get_json(force=True)
        
        print("Received JSON:", json_data)
        print("Action:", action)

        # store the data based on action type
        if Action(action.upper()) == Action.push:
            # parse the input data to push payload
            payload_data = WebhookPayload(**json_data)
            # store the data in database for push action
            data = await WebhookService.store_data(payload_data, Action.push)
        elif Action(action.upper()) == Action.pull_request:
            # parse the input data to pull request payload
            payload_data = PullRequestWebhookPayload(**json_data)
            # check if its a merge or pull request action
            if not payload_data.pull_request.merged:
              # store the data in database for pull request action
              data = await WebhookService.store_data(payload_data, Action.pull_request)
            else:
              # store the data in database for merge action
              data = await WebhookService.store_data(payload_data, Action.merge)
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return {"error": str(e)}, 400

    if not data:
        return {}, 500
    return {}, 200

