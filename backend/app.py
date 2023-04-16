import flask
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from flask_cors import CORS

from resources import config
from resources import init_routes
from database.db import create_db

# create flask app
app = flask.Flask(__name__)

# init app
config.init_cfg(app)

# init routes
init_routes.init(app)

# init jwt
jwt = JWTManager(app)

# init swagger
Swagger(app)

# init cors
CORS(app)


# init db
@app.before_first_request
def create_tables():
    create_db(app, jwt)


# run app
if __name__ == '__main__':
    app.run(debug=True)
