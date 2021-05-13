from application.db import db
from sqlalchemy.sql import func
import navigation.navigation_calculations as dis
from application.models.location_model import LocationModel
from navigation.cal_mag_deviation import CalculateMagenticDeviation as MagDev


class CourseModel(db.Model):
    __tablename__ = 'courses'
    hash_key = db.Column(db.String(80), primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    date = db.Column(db.String(80), default=func.to_char(func.today, '%Y-%m-%d'))

    start_name = db.Column(db.String(80), db.ForeignKey('locations.name'), nullable=False)
    start = db.relationship('LocationModel', foreign_keys=start_name)

    end_name = db.Column(db.String(80), db.ForeignKey('locations.name'), nullable=False)
    end = db.relationship('LocationModel', foreign_keys=end_name)

    map_course = db.Column(db.Float(precision=1))
    compass_course = db.Column(db.Float(precision=1))
    nautical_mile = db.Column(db.Float(precision=1))

    def __init__(self, date, start_name, end_name):
        self.hash_key = self.create_hash_key(date, start_name, end_name)
        self.date = date
        self.start_name = start_name
        self.end_name = end_name
        self.map_course = self.get_map_couse()
        self.compass_course = self.get_compass_course()
        self.nautical_mile = self.get_nautical_mile()

    def get_nautical_mile(self):
        start_location = LocationModel.find_by_name(self.start_name)
        end_location = LocationModel.find_by_name(self.end_name)
        return dis.calculate_nautical_mile(self.convert_locationmodel_to_geolocation(start_location),
                                           self.convert_locationmodel_to_geolocation(end_location))

    def get_map_couse(self):
        start_location = LocationModel.find_by_name(self.start_name)
        end_location = LocationModel.find_by_name(self.end_name)
        return dis.calculate_map_course_from_start_end(self.convert_locationmodel_to_geolocation(start_location),
                                                       self.convert_locationmodel_to_geolocation(end_location))

    def get_compass_course(self):
        map_course = self.get_map_couse()
        start_location = LocationModel.find_by_name(self.start_name)
        start_geo_location = self.convert_locationmodel_to_geolocation(start_location)
        course = dis.SailingCourse(start_geo_location.name, start_geo_location.latitude,
                                   start_geo_location.longitude, map_course=map_course, date=self.date)
        mag_dev = MagDev()
        return dis.cal_compass_course(course, mag_dev)

    @staticmethod
    def create_hash_key(date, start_name, end_name):
        return hash((date, start_name, end_name))

    @staticmethod
    def convert_locationmodel_to_geolocation(loc: LocationModel):
        return dis.GeoLocation(name=loc.name, latitude=loc.latitude, longitude=loc.longtitude)

    def json(self):
        return {'start_name': self.start_name, 'end_name': self.end_name,
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
        return {date: [course.json() for course in cls.query.filter_by(date=date).all()]}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
