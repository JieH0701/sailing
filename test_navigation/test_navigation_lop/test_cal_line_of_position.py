import pytest
from collections import namedtuple
from navigation.cal_ship_position import CalculateShipPosition

position = namedtuple('position', 'name latitude longitude')
LoP = namedtuple('LOP', 'location copass_course slop intercept')


@pytest.fixture(scope='module')
def cal_lop(compass_course=225, location=position(name='test_navigation', latitude=15, longitude=15)
            , devication_table_path='navigation/magnetic_deviation_table.csv'):
    return CalculateShipPosition(compass_course, location, devication_table_path)


def test_cal_line_vector(cal_lop):
    lop = cal_lop.cal_line_vector()
    assert (lop == LoP(position('test_navigation', 15, 15), 225, 0.6, 6.0))
