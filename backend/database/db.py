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

    basedir = os.path.abspath(os.path.dirname(__file__))
    if not os.path.exists(basedir + '/../instance/db.sqlite'):
        from database.model.admin import Admin
        from database.model.image_counter import ImageCounter
        db.create_all()
        db.session.add(Admin(username='admin', password='admin'))
        db.session.add(Admin(username='user', password='user', admin_type="super_admin"))
        db.session.add(ImageCounter())
        db.session.commit()
        print('Database created!')
    else:
        db.create_all()
