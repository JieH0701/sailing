from application.db import db
from sqlalchemy.sql import func


class CourseModel(db.Model):
    __tablename__ = 'courses'
    hash_key = db.Column(db.String(80), primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    date = db.Column(db.Date, default=func.today())

    start_name = db.Column(db.String(80), db.ForeignKey('locations.name'), nullable=False)
    start = db.relationship('LocationModel', foreign_keys=start_name)

    end_name = db.Column(db.String(80), db.ForeignKey('locations.name'), nullable=False)
    end = db.relationship('LocationModel', foreign_keys=end_name)

    map_course = db.Column(db.Float(precision=1))
    compass_course = db.Column(db.Float(precision=1))

    def __init__(self, date, start_name, end_name):
        self.hash_key = self.create_hash_key(date, start_name, end_name)
        self.date = date
        self.start_name = start_name
        self.end_name = end_name

    @staticmethod
    def create_hash_key(date, start_name, end_name):
        return hash((date, start_name, end_name))

    def json(self):
        return {'timestamp': self.timestamp, 'start_name': self.start_name, 'end_name': self.end_name,
                'map_course': self.map_course, 'compass_course': self.compass_course}

    @classmethod
    def find_course(cls, date, start_time, end_time):
        hasd_key = cls.create_hash_key(date, start_time, end_time)
        return cls.query.filter_by(hash_key=hasd_key).first()

    @classmethod
    def find_by_start_name(cls, start_name):
        return {start_name: [course.json() for course in cls.query.filter_by(name=start_name).all()]}

    @classmethod
    def find_by_end_name(cls, end_name):
        return {end_name: [course.json() for course in cls.query.filter_by(name=end_name).all()]}

    @classmethod
    def find_by_date(cls, date):
        return {date: [course.json() for course in cls.query.filter_by(name=date).all()]}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
