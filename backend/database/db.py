import os

from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()


def create_db(app, jwt):
    db.init_app(app)

    from database.model.token import TokenBlocklist

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

        return token is not None

    if not os.path.exists('instance/db.sqlite'):
        from database.model.admin import Admin
        db.create_all()
        db.session.add(Admin(username='admin', password='admin'))
        db.session.commit()
        print('Database created!')
    else:
        db.create_all()
