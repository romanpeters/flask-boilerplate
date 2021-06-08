#!flask/bin/python
import os
from app import app
import random

if not os.path.exists('data'):
    os.makedirs('data')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
