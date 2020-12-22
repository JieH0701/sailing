from geopy.distance import geodesic, great_circle
import geomag
import math
from collections import namedtuple
import numpy as np


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


def cal_magnetic_declination(latitude, longitude):
    declination = geomag.declination(float(latitude), float(longitude))
    return round(declination, 2)


def cal_course_with_magnetic_declination(map_course, latitude, longitude):
    course_with_declination = geomag.mag_heading(float(map_course), float(latitude), float(longitude))
    return round(course_with_declination, 2)


def cal_interp(x1, y1, x2, y2, x0):
    x = [x1, x2]
    y = [y1, y2]
    return np.interp(x0, x, y)


def cal_line_vector(course, location):
    LoP = namedtuple('LOP', 'location course slop intercept')
    angle = 90 - (course % 90)  # get the degree from map_course between 0-90
    slop = round(math.cos(math.radians(angle)), 2)
    intercept = round(location.longitude - slop * location.latitude, 2)
    return LoP(location=location.name, course=course, slop=slop, intercept=intercept)


def cal_position_fix(lop1, lop2):
    geo_position = namedtuple('geo_position', 'name latitude longitude')
    if lop1.slop == lop2.slop:
        print("This two place are parallel")
        return geo_position('myPosition', 0, 0)
    else:
        mylatitude = (lop2.intercept - lop1.intercept) / (lop1.slop - lop2.slop)
        mylongtitude = lop1.slop * mylatitude + lop1.intercept
        return geo_position('Fix Position', mylatitude, mylongtitude)


def cal_position_triangle(lop1, lop2, lop3):
    p1 = cal_position_fix(lop1, lop2)
    p2 = cal_position_fix(lop2, lop3)
    p3 = cal_position_fix(lop1, lop3)
    return ('Middle of Triangel', (p1.latitude + p2.latitude + p3.latitude) / 3,
            (p1.longitude + p2.longitude + p3.longitude) / 3)
