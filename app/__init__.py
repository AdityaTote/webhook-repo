from flask import Flask
from flask_cors import CORS

from app.api.webhook import webhook
from app.api.github import github


# Creating our flask app
def create_app():

    app = Flask(__name__, static_folder='../static', static_url_path='/static')
    
    CORS(app)
    
    # registering all the blueprints
    app.register_blueprint(webhook)
    app.register_blueprint(github)
    
    return app
