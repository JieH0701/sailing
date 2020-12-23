from navigation.navigation_calculations import Location, cal_course_line, cal_position_fix, cal_position_triangle


class CalculateShipPosition:
    def __init__(self, loc1: Location, loc2: Location, loc3: Location = None):
        self.lop1 = cal_course_line(loc1)
        self.lop2 = cal_course_line(loc2)
        if loc3 is not None:
            self.lop3 = cal_course_line(loc3)
            self.res = cal_position_triangle(self.lop1, self.lop2, self.lop3)
        else:
            self.res = cal_position_fix(self.lop1, self.lop2)

    def __str__(self):
        pass
