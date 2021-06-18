import secrets
from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe()
bootstrap = Bootstrap(app)

from app import views, api
