from urllib.parse import urlparse
from flask import request, jsonify, abort

from app import app


@app.route("/api/", methods=['GET'])
def endpoints():
    """Overview of the API endpoints."""
    return jsonify({'endpoints': endpoints})



endpoints = [{"path": "/api/",
              "name": endpoints.__name__,
              "method": "GET",
              "description": endpoints.__doc__},
             ]

