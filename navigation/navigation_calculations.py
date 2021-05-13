from geopy.distance import geodesic, great_circle
import geomag
import math
from dataclasses import dataclass, replace
from navigation.cal_mag_deviation import CalculateMagenticDeviation
from datetime import datetime


@dataclass()
class GeoLocation:
    name: str
    latitude: float
    longitude: float


@dataclass()
class SailingCourse(GeoLocation):
    map_course: float = None
    compass_course: float = None
    nautical_mile: float = None
    date: str = None


@dataclass()
class LoP:
    name: str
    slop: float
    intercept: float


def convert_str_to_date(date_str: str):
    return datetime.strptime(date_str, '%Y-%m-%d').date()


def calculate_nautical_mile(start: GeoLocation, end: GeoLocation, method='geodesic'):
    if method == 'great_circle':
        dis = great_circle((start.latitude, start.longitude), (end.latitude, end.longitude)).nm
    else:
        dis = geodesic((start.latitude, start.longitude), (end.latitude, end.longitude)).nm
    return round(dis, 2)


def calculate_map_course_from_start_end(start: GeoLocation, end: GeoLocation):
    lat1 = math.radians(start.latitude)
    lat2 = math.radians(end.latitude)
    diff_long = math.radians(end.longitude - start.longitude)
    x = math.sin(diff_long) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diff_long))
    course = math.atan2(x, y)
    # Now we have the initial course but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass course
    # The solution is to normalize the initial course as shown below
    course = math.degrees(course)
    compass_bearing = (course + 360) % 360
    return round(compass_bearing, 2)


def cal_magnetic_declination(course: SailingCourse):
    declination = geomag.declination(course.latitude, course.longitude, time=convert_str_to_date(course.date))
    return round(declination)


def cal_compass_course(course: SailingCourse, deviation: CalculateMagenticDeviation):
    declination = cal_magnetic_declination(course)
    deviation = deviation.cal_deviation(course.map_course, 'map')
    compas_course = course.map_course - declination - deviation
    return int(compas_course)


def cal_map_course(course: SailingCourse, deviation: CalculateMagenticDeviation):
    declination = cal_magnetic_declination(course)
    deviation = deviation.cal_deviation(course.compass_course, 'compass')
    map_course = course.compass_course + declination + deviation
    return int(map_course)


def cal_course_line(course: SailingCourse):
    angle = course.map_course - (course.map_course // 90) * 90  # get the degree from map_course between 0-90
    slop = round(math.sin(math.radians(angle)), 2)
    intercept = round(course.longitude - slop * course.latitude, 2)
    return LoP(name=course.name, slop=slop, intercept=intercept)


def fill_location_course(course: SailingCourse, deviation: CalculateMagenticDeviation):
    if course.map_course is None:
        map_course = cal_map_course(course, deviation)
        return replace(course, map_course=map_course)
    else:
        compass_course = cal_compass_course(course, deviation)
        return replace(course, compass_course=compass_course)


def check_course_in_compas_range(course):
    if 0 <= course < 360:
        return course
    else:
        print(f'The course input {course} is wrong, use default vaule 0')
        return None


def cal_position_fix(lop1: LoP, lop2: LoP):
    if lop1.slop == lop2.slop:
        print("This two place are parallel")
        return GeoLocation('myPosition', 0, 0)
    else:
        mylatitude = (lop2.intercept - lop1.intercept) / (lop1.slop - lop2.slop)
        mylongtitude = lop1.slop * mylatitude + lop1.intercept
        return GeoLocation('Fix Position', round(mylatitude, 2), round(mylongtitude, 2))


def cal_position_triangle(lop1: LoP, lop2: LoP, lop3: LoP):
    p1 = cal_position_fix(lop1, lop2)
    p2 = cal_position_fix(lop2, lop3)
    p3 = cal_position_fix(lop1, lop3)
    return GeoLocation('Middle of Triangel', (p1.latitude + p2.latitude + p3.latitude) / 3,
                       (p1.longitude + p2.longitude + p3.longitude) / 3)
