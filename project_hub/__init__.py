import os
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
import redis


app = Flask(__name__)

load_dotenv()
db_user = os.getenv('PHUB_USER')
db_pass = os.getenv('PHUB_PASSWORD')
db_name = os.getenv('PHUB_DATABASE')
db_host = os.getenv('HOST')
db_port = os.getenv('PORT')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
app.app_context().push()
app.config['UPLOAD_FOLDER'] = 'static/images/'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'hub:'
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')

Session(app)

login_manager = LoginManager()
login_manager.init_app(app)


db = SQLAlchemy(app)

migrate = Migrate(app, db)

from api.v1.views import app_views
app.register_blueprint(app_views, url_prefix='/api/v1/')

from project_hub.models.user import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

import project_hub.models.views.projects
import project_hub.models.views.registration
