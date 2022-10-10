import os
from app import sqlalchemy as sa
from app import login_manager as lm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

"""
https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
"""

class User(sa.Model, UserMixin):
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(80), unique=True, nullable=False)
    email = sa.Column(sa.String(120), unique=True)
    password_hash = sa.Column(sa.String(100))
    first_name = sa.Column(sa.String(80))
    last_name = sa.Column(sa.String(80))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

