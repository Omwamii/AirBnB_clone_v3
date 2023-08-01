#!/usr/bin/python3
""" module: return status of API
"""
from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def page_not_found(error):
    """ render json 'not found'
    """
    err = {"error": "Not found"}
    return jsonify(err)


@app.teardown_appcontext
def teardown_db(res_or_except):
    """ remove the currenct SQLAlchemy session
    """
    storage.close()


if __name__ == "__main__":
    from os import environ as env
    env_host, env_port = env.get('HBNB_API_HOST'), env.get('HBNB_API_PORT')
    host = env_host if env_host else '0.0.0.0'
    port = env_port if env_port else '5000'
    app.run(host=host, port=int(port), threaded=True)
