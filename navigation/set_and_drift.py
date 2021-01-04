from dataclasses import dataclass
from navigation.cal_mag_deviation import CalculateMagenticDeviation
import math
from collections import namedtuple


@dataclass()
class Storm:
    direction: int
    speed: float


def cal_course_over_water_from_compass_course(compass_course, declination, deviation: CalculateMagenticDeviation, wind):
    return compass_course + deviation.cal_deviation(compass_course, 'compass') + declination + wind


def cal_pos(angle, dis):
    pos = namedtuple('pos', 'x, y')
    x = round(math.sin(math.radians(angle)) * dis, 2)
    y = round(math.cos(math.radians(angle)) * dis, 2)
    return pos(x, y)


def cal_ground_track(course_over_water, log, storm):
    coupling_location = cal_pos(course_over_water, log)
    storm_pos = cal_pos(storm.direction, storm.speed)
    x = coupling_location.x + storm_pos.x
    y = coupling_location.y + storm_pos.y
    ground_track = math.sqrt(x * x + y * y)
    course_over_ground = math.tan(x / y)
    return ground_track, course_over_ground


def cal_compass_course_to_destination(map_course, distance, storm, log):
    pass
