import secrets
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/sqlite.db'

bootstrap = Bootstrap(app)
sqlalchemy = SQLAlchemy(app)

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "index"
# login_manager.login_message = "Please login first."

from app import views, api, errors
