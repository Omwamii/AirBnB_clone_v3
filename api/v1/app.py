#!/usr/bin/python3
""" module: return status of API
"""
from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown_db(res_or_except):
    """ remove the currenct SQLAlchemy session
    """
    storage.close()


if __name__ == "__main__":
    from os import environ as env
    if env.get('HBNB_API_HOST'):
        host = env.get('HBNB_API_HOST')
    else:
        host = '0.0.0.0'
    if env.get('HBNB_API_PORT'):
        port = env.get('HBNB_API_PORT')
    else:
        port = '5000'
    app.run(host=host, port=int(port), threaded=True)
