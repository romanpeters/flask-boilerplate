from app import sqlalchemy as sa

"""
https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
"""

class User(sa.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(80), unique=True, nullable=False)
    email = sa.Column(sa.String(120), unique=True)
    first_name = sa.Column(sa.String(80))
    last_name = sa.Column(sa.String(80))

    def __repr__(self):
        return '<User %r>' % self.username


sa.create_all()
