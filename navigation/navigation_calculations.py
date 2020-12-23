from geopy.distance import geodesic, great_circle
import geomag
import math
from dataclasses import dataclass, replace
from datetime import date
from navigation.cal_mag_deviation import CalculateMagenticDeviation


@dataclass()
class GeoPosition:
    name: str
    latitude: float
    longitude: float


@dataclass()
class Location(GeoPosition):
    map_course: float = None
    compass_course: float = None
    time: date = date.today()


@dataclass()
class LoP:
    name: str
    slop: float
    intercept: float


def calculate_nautical_mile(start, end, method='geodesic'):
    if method == 'great_circle':
        dis = great_circle((start.latitude, start.longitude), (end.latitude, end.longitude)).nm
    else:
        dis = geodesic((start.latitude, start.longitude), (end.latitude, end.longitude)).nm
    return round(dis, 2)


def calculate_map_course_from_start_end(start, end):
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


def cal_magnetic_declination(location: Location):
    declination = geomag.declination(location.latitude, location.longitude, time=location.time)
    return round(declination)


def cal_compass_course(location: Location, deviation: CalculateMagenticDeviation):
    declination = cal_magnetic_declination(location)
    deviation = deviation.cal_deviation(location.map_course, 'map')
    compas_course = location.map_course - declination - deviation
    return int(compas_course)


def cal_map_course(location: Location, deviation: CalculateMagenticDeviation):
    declination = cal_magnetic_declination(location)
    deviation = deviation.cal_deviation(location.compass_course, 'compass')
    map_course = location.compass_course + declination + deviation
    return int(map_course)


def cal_course_line(loc: Location):
    angle = (loc.map_course // 90) * 90 + loc.map_course  # get the degree from map_course between 0-90
    slop = round(math.sin(math.radians(angle)), 2)
    intercept = round(loc.longitude - slop * loc.latitude, 2)
    return LoP(name=loc.name, slop=slop, intercept=intercept)


def fill_location_course(location: Location, deviation: CalculateMagenticDeviation):
    if location.map_course is None:
        map_course = cal_map_course(location, deviation)
        return replace(location, map_course=map_course)
    else:
        compass_course = cal_compass_course(location, deviation)
        return replace(location, compass_course=compass_course)


def check_course_in_compas_range(course):
    if 0 <= course < 360:
        return course
    else:
        print(f'The course input {course} is wrong, use default vaule 0')
        return None


def cal_position_fix(lop1: LoP, lop2: LoP):
    if lop1.slop == lop2.slop:
        print("This two place are parallel")
        return GeoPosition('myPosition', 0, 0)
    else:
        mylatitude = (lop2.intercept - lop1.intercept) / (lop1.slop - lop2.slop)
        mylongtitude = lop1.slop * mylatitude + lop1.intercept
        return GeoPosition('Fix Position', round(mylatitude, 2), round(mylongtitude, 2))


def cal_position_triangle(lop1: LoP, lop2: LoP, lop3: LoP):
    p1 = cal_position_fix(lop1, lop2)
    p2 = cal_position_fix(lop2, lop3)
    p3 = cal_position_fix(lop1, lop3)
    return GeoPosition('Middle of Triangel', (p1.latitude + p2.latitude + p3.latitude) / 3,
                       (p1.longitude + p2.longitude + p3.longitude) / 3)
