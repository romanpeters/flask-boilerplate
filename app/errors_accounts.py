from flask import render_template
from app import app, login_manager


@login_manager.unauthorized_handler
def unauthorized():
    return render_template("index.html"), 401
