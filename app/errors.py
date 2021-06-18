from flask import render_template
from app import app, login_manager


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@login_manager.unauthorized_handler
def unauthorized():
    return render_template('index.html'), 401
