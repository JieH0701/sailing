import navigation.get_geo_position as geo
import navigation.navigation_calculations as dis
from navigation.cal_mag_deviation import CalculateMagenticDeviation as MagDev


def main(name, start_position, end_position):
    mygeo = geo.GetGeoPosition(name)
    start = mygeo.get_geo_position(start_position)
    end = mygeo.get_geo_position(end_position)

    distance = dis.calculate_nautical_mile(start, end)
    map_course = dis.calculate_map_course_from_start_end(start, end)

    course_with_declination = dis.cal_course_with_magnetic_declination(map_course, start.latitude, start.longitude)

    course_with_devication = MagDev(course_with_declination, 'magnetica course').cal_course_with_deviation()

    nautical_mile = f'The distance between {start_position} and {end_position} is {distance} nautical mile. \n'
    map_course = f'The map course between {start_position} and {end_position} is {map_course} Grad. \n'
    compass_course = f'The compass course, including magnetic declination and magnetic deviation ' \
                     f'is {course_with_devication} Grad. \n'

    print(nautical_mile + map_course + compass_course)


if __name__ == '__main__':
    appname = 'Sailing'
    print(f'Hi, this is my {appname} application. Just for fun!')
    main(appname, 'Marina Grado', 'Marina Venedig')
