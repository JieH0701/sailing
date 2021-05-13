import pytest
import navigation.cal_ship_position as pos
from navigation.navigation_calculations import SailingCourse, GeoLocation


@pytest.fixture(scope='module')
def ship_position():
    loc1 = SailingCourse(name='Accumer', latitude=53.47, longitude=7.29, compass_course=309, map_course=317,
                         date='2013-08-14')
    loc2 = SailingCourse(name='Wasserturm Langeoog', latitude=53.43, longitude=7.28, compass_course=221, map_course=229,
                         date='2013-08-14')
    return pos.CalculateShipPosition(loc1, loc2)


def test_ship_position(ship_position):
    assert (ship_position.get_ship_position() == GeoLocation('Fix Position', 52.5, 6.58))
