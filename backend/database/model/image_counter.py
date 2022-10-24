from database.db import db


# Counter model
class ImageCounter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    counter = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<Counter %r>' % self.counter
