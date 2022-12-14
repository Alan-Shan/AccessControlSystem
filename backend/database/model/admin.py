from database.db import db


# admin model
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    admin_type = db.Column(db.String(15), nullable=False, default='admin')

    refresh_token = db.Column(db.String(100), nullable=True, default='')
    access_token = db.Column(db.String(100), nullable=True, default='')

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'admin_type': self.admin_type,
        }

    def __repr__(self):
        return '<User %r>' % self.username
