from database.db import db


# User model
class VisitRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    patronymic = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)

    image_path = db.Column(db.String(80), nullable=True, default=None)

    # document (passport or driver license)
    document_type = db.Column(db.String(20), nullable=False)
    document_number = db.Column(db.String(10), nullable=False)

    purpose = db.Column(db.String(120), nullable=False)

    approved = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<User %r>' % self.username
