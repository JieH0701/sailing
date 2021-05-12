from application.db import db
import navigation.get_geo_position as geo


class LocationModel(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    latitude = db.Column(db.Float(precision=2))
    longtitude = db.Column(db.Float(precision=2))

    def __init__(self, name, longtitude, latitude):
        self.name = name
        self.longtitude = longtitude
        self.latitude = latitude

    def json(self):
        return {'name': self.name, 'latitude': self.latitude, 'longtitude': self.longtitude}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @staticmethod
    def get_location_by_name(name):
        geo_position = geo.GetGeoPosition("application").get_geo_position(name)
        location = LocationModel(name, geo_position.longitude, geo_position.latitude)
        return location

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
