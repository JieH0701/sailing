import navigation.navigation_calculations as dis


class CalculateShipPosition:
    def __init__(self, course1, location1, course2, location2, course3=None, location3=None):
        self.loc1 = dis.cal_line_vector(course1, location1)
        self.loc2 = dis.cal_line_vector(course2, location2)
        if course3 is not None:
            self.loc3 = dis.cal_line_vector(course3, location3)
            self.res = dis.cal_position_triangle(self.loc1, self.loc2, self.loc3)
        else:
            self.fuc = dis.cal_position_fix(self.loc1, self.loc2)

    def __str__(self):
        pass
