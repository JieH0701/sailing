import pandas as pd
import numpy as np


class CalculateMagenticDeviation:
    def __init__(self, path='navigation/magnetic_deviation_table.csv'):
        self.__deviation = pd.read_csv(path, header=0)
        self.__courses = self.__deviation.compass_course.to_list()
        self.__devication_mc = {self.__courses[i]: self.__deviation.deviation_mc.to_list()[i]
                                for i in range(len(self.__courses))}
        self.__devication_cc = {self.__courses[i]: self.__deviation.deviation_cc.to_list()[i]
                                for i in range(len(self.__courses))}

    def __cal_deviation(self, deviation_table, course):
        if course in self.__courses:
            devication = deviation_table.get(course)
            return devication
        else:
            course_range = cal_course_from_num(course)
            lower_devication = deviation_table.get(course_range[0])
            upper_devication = deviation_table.get(course_range[1])
            devication = cal_interp(
                course_range[0], lower_devication, course_range[1], upper_devication, course)
            return devication

    def cal_deviation(self, course, method):
        if method == 'compass':
            return CalculateMagenticDeviation.__cal_deviation(self, self.__devication_cc, int(course))
        else:
            return CalculateMagenticDeviation.__cal_deviation(self, self.__devication_mc, int(course))


def cal_course_from_num(num):
    num = int(str(round(num))[:-1])
    upper = (num + 1) * 10
    lower = num * 10
    return upper, lower


def cal_interp(x1, y1, x2, y2, x0):
    x = [x1, x2]
    y = [y1, y2]
    return np.interp(x0, x, y)
