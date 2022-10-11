import secrets
from flask import Flask
from flask_bootstrap import Bootstrap5
#from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager

app = Flask(__name__)

## uncomment for account management
#login_manager = LoginManager()
#login_manager.login_view = "index"
#login_manager.login_message = "Please login first."

with app.app_context():
    app.secret_key = secrets.token_urlsafe()
    bootstrap = Bootstrap5(app)
## uncomment for database + account management
#    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+pysqlite:///sqlite.db'
#    sqlalchemy = SQLAlchemy(app)
#    login_manager.init_app(app)

from app import views, api, errors

## uncomment for account management
# from app import views_accounts, errors_accounts

#with app.app_context():
#    sqlalchemy.create_all()
