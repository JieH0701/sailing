import pandas as pd
from navigation.navigation_calculations import cal_interp


class CalculateMagenticDeviation:
    def __init__(self, course_input, method='compass course', path='navigation/magnetic_deviation_table.csv'):
        self.path = path
        self.deviation = pd.read_csv(path, header=0)
        self.compass_course = self.deviation.compass_course.to_list()
        self.devication_mc = {self.compass_course[i]: self.deviation.deviation_mc.to_list()[i]
                              for i in range(len(self.compass_course))}
        self.devication_cc = {self.compass_course[i]: self.deviation.deviation_cc.to_list()[i]
                              for i in range(len(self.compass_course))}
        self.method = method
        if 0 <= course_input < 360:
            self.course_input = int(course_input)
        else:
            print(f'The course input {course_input} is wrong, use default vaule 0')
            self.course_input = 0

    def cal_deviation(self, deviation_table):
        if round(self.course_input) in self.compass_course:
            devication = deviation_table.get(self.course_input)
            return devication
        else:
            course_range = cal_course_from_num(self.course_input)
            lower_devication = deviation_table.get(course_range[0])
            upper_devication = deviation_table.get(course_range[1])
            devication = cal_interp(
                course_range[0], lower_devication, course_range[1], upper_devication, self.course_input)
            return devication

    def cal_course_with_deviation(self):
        if self.method == 'compass':
            return CalculateMagenticDeviation.cal_deviation(self, self.devication_mc) + self.course_input
        else:
            return self.course_input - CalculateMagenticDeviation.cal_deviation(self, self.devication_mc)


def cal_course_from_num(num):
    num = int(str(round(num))[:-1])
    upper = (num + 1) * 10
    lower = num * 10
    return upper, lower
