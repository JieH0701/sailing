from geopy.geocoders import Nominatim
import NauticalInformation.CalculateGeoDistance as Geo
import NauticalInformation.CalculateMagenticDeviation as Devi


def main(appname, start_position, end_position):
    devication_table_path = 'NauticalInformation/magnetic_deviation_table.csv'
    geolocator = Nominatim(user_agent=appname)

    mygeo = Geo.CalculateGeoDistance(geolocator)
    start = mygeo.get_geo_position(start_position)
    end = mygeo.get_geo_position(end_position)

    distance = mygeo.calculate_nautical_mile(start, end)
    map_course = mygeo.calculate_map_course(start, end)

    course_with_declination = mygeo.cal_course_with_magnetic_declination(float(map_course), start)
    course_with_devication = Devi.CalculateMagenticDeviation(
        devication_table_path, float(course_with_declination), 'magnetica_course').cal_course_with_deviation()

    nautical_mile = f'The distance between {start_position} and {end_position} is {distance} nautical mile. \n'
    map_course = f'The map course between {start_position} and {end_position} is {map_course} Grad. \n'
    compass_course = f'The compass course, including magnetic declination and magnetic deviation ' \
                     f'is {course_with_devication} Grad. \n'

    print(nautical_mile + map_course + compass_course)


if __name__ == '__main__':
    name = 'Sailing'
    print(f'Hi, this is my {name} application. Just for fun!')
    main(name, 'Marina Grado', 'Marina Venedig')
