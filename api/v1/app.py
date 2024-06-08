from flask import Flask
from dotenv import load_dotenv
import os
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from project_hub import app, db

CORS(app, resources={r"/api/*": {"origins": "*"}})


from project_hub.models.user import User
