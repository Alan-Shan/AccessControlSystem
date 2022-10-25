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

    status = db.Column(db.String(20), nullable=False, default="pending")

    creation_time = db.Column(db.DateTime, nullable=False, default=db.func.now())
    update_time = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'patronymic': self.patronymic,
            'email': self.email,
            'phone': self.phone,
            'image_path': self.image_path,
            'document_type': self.document_type,
            'document_number': self.document_number,
            'purpose': self.purpose,
            'status': self.status,
            "creation_time": self.creation_time,
            "update_time": self.update_time
        }

    def __repr__(self):
        return '<User %r>' % self.username
