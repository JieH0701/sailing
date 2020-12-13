from geopy.geocoders import Nominatim
import NauticalInformation.CalculateGeoDistance as Geo


def print_application_name(name):
    print(f'Hi, this is my {name} application. Just for fun!')


def get_geo_position(appname):
    geolocator = Nominatim(user_agent=appname)
    return geolocator


if __name__ == '__main__':
    app = 'Sailing courses'
    print_application_name(app)
    mygeolocator = get_geo_position(app)
    mygeo = Geo.CalculateGeoDistance(mygeolocator)
    start = mygeo.get_geo_position('Marina Grado')
    end = mygeo.get_geo_position('Marina Venedig')
    print(mygeo.get_str_for_nautical_courses(start, end))
