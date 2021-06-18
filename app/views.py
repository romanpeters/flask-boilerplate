from flask import render_template, redirect, request
from app import app
from app import database

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")
