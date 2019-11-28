from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
from twilio.rest import Client
import os
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from config import Config
from flask_login import LoginManager

# from flask_admin import Admin

load_dotenv(find_dotenv())

app = Flask(__name__)
# admin = Admin(app, name="microblog", template_mode="bootstrap3")
app.config.from_object(Config)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
mail = Mail(app)
message_client = Client(os.getenv("SID"), os.getenv("AUTH"))
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from entrymanagement import routes
