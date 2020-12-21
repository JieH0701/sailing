from dataclasses import dataclass
from geopy.distance import geodesic
from geopy.distance import great_circle
import geomag
import math


@dataclass()
class GeoPosition:
    name: str
    latitude: float
    longitude: float


class CalculateGeoDistance:
    def __init__(self, geolocator):
        self.geolocator = geolocator

    def get_geo_position(self, address_name):
        position = self.geolocator.geocode(address_name)
        geoposition: GeoPosition = GeoPosition(address_name, position.latitude, position.longitude)
        return geoposition

    @staticmethod
    def calculate_nautical_mile(start: GeoPosition, end: GeoPosition, method='geodesic'):
        if method == 'great_circle':
            dis = great_circle((start.latitude, start.longitude), (end.latitude, end.longitude)).nm
        else:
            dis = geodesic((start.latitude, start.longitude), (end.latitude, end.longitude)).nm
        return "{:.2f}".format(dis)

    @staticmethod
    def calculate_map_course(start, end):
        lat1 = math.radians(start.latitude)
        lat2 = math.radians(end.latitude)
        diff_long = math.radians(end.longitude - start.longitude)
        x = math.sin(diff_long) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diff_long))
        bearing = math.atan2(x, y)
        # Now we have the initial bearing but math.atan2 return values
        # from -180° to + 180° which is not what we want for a compass bearing
        # The solution is to normalize the initial bearing as shown below
        bearing = math.degrees(bearing)
        compass_bearing = (bearing + 360) % 360
        return "{:.2f}".format(compass_bearing)

    @staticmethod
    def cal_course_with_magnetic_declination(map_course, start: GeoPosition):
        return geomag.mag_heading(map_course, start.latitude, start.longitude)


