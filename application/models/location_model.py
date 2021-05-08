from application.db import db


class LocationModel(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    latitude = db.Column(db.Float(precision=2))
    longtitude = db.Column(db.Float(precision=2))

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    cource = db.relationship('CourseModel')

    def __init__(self, name, longtitude, latitude):
        self.name = name
        self.longtitude = longtitude
        self.latitude = latitude

    def json(self):
        return {'name': self.name, 'latitude': self.latitude, 'longtitude': self.longtitude}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()



