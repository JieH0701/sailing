from geopy.geocoders import Nominatim
from collections import namedtuple


class GetGeoPosition:
    def __init__(self, appname, geocoders=Nominatim):
        self.geolocator = geocoders(user_agent=appname)

    def get_geo_position(self, address_name):
        geo_position = namedtuple('geo_position', 'name latitude longitude')
        position = self.geolocator.geocode(address_name)
        geoposition = geo_position(name=address_name, latitude=position.latitude
                                   , longitude=position.longitude)
        return geoposition
