import os
from datetime import timedelta


def init_cfg(app):
    # JWT config
    app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    # SQL Alchemy config
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, '../instance/db.sqlite')

    # CORS config
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['CORS_RESOURCES'] = {r"/*": {"origins": "*"}}
    app.config['CORS_SUPPORTS_CREDENTIALS'] = True

    # change swagger template
    app.config['SWAGGER'] = {
        'title': 'Access Control System API',
        'version': '1.0.0',
        'uiversion': 3,
        'specs_route': '/api/docs/',
        'specs': [
            {
                'endpoint': 'apispec',
                'route': '/api/docs/apispec.json',
            }
        ]
    }
