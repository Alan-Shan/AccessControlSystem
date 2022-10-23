from datetime import timedelta


def init_cfg(app):
    # JWT config
    ACCESS_EXPIRES = timedelta(hours=1)
    app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES

    # SQL Alchemy config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
