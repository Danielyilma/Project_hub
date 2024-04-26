import os
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


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

login_manager = LoginManager()
login_manager.init_app(app)


db = SQLAlchemy(app)

from project_hub.models.user import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from project_hub.view import home
