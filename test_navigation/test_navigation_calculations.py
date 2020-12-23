import pytest
import navigation.navigation_calculations as dis
from navigation.cal_mag_deviation import CalculateMagenticDeviation
from datetime import datetime


@pytest.fixture(scope='module')
def start():
    return dis.GeoPosition(name='Accumer', latitude=53.47, longitude=7.29)


@pytest.fixture(scope='module')
def end():
    return dis.GeoPosition(name='Wasserturm Langeoog', latitude=53.43, longitude=7.28)


@pytest.fixture(scope='module')
def accumer(start):
    return dis.Location(start.name, start.latitude, start.longitude, compass_course=309, map_course=317,
                        time=datetime.strptime('2013-08-14', '%Y-%m-%d').date())


@pytest.fixture(scope='module')
def wasserturm(end):
    return dis.Location(end.name, end.latitude, end.longitude, compass_course=221, map_course=229,
                        time=datetime.strptime('2013-08-14', '%Y-%m-%d').date())


@pytest.fixture(scope='module')
def deviation():
    return CalculateMagenticDeviation()


def test_calculate_nautical_mile(start, end):
    assert (dis.calculate_nautical_mile(start, end) == 2.43)


def test_calculate_map_course_from_start_end(start, end):
    assert (dis.calculate_map_course_from_start_end(start, end) == 188.47)


def test_cal_magnetic_declination(wasserturm):
    assert (dis.cal_magnetic_declination(wasserturm) == 1)


def test_cal_line_vector(accumer, wasserturm):
    assert (dis.cal_course_line(accumer) == dis.LoP('Accumer', -0.73, 46.32))
    assert (dis.cal_course_line(wasserturm) == dis.LoP('Wasserturm Langeoog', 0.75, -32.79))


def test_cal_position_fix(accumer, wasserturm):
    assert (dis.cal_position_fix(dis.cal_course_line(accumer), dis.cal_course_line(wasserturm))
            == dis.GeoPosition('Fix Position', 53.45, 7.3))
