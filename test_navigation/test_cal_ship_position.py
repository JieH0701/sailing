import pytest
import navigation.cal_ship_position as pos
from navigation.navigation_calculations import Location, GeoPosition
from datetime import datetime


@pytest.fixture(scope='module')
def ship_position():
    loc1 = Location(name='Accumer', latitude=53.47, longitude=7.29, compass_course=309, map_course=317,
                    time=datetime.strptime('2013-08-14', '%Y-%m-%d').date())
    loc2 = Location(name='Wasserturm Langeoog', latitude=53.43, longitude=7.28, compass_course=221, map_course=229,
                    time=datetime.strptime('2013-08-14', '%Y-%m-%d').date())
    return pos.CalculateShipPosition(loc1, loc2)


def test_ship_position(ship_position):
    assert (ship_position.get_ship_position() == GeoPosition('Fix Position', 53.45, 7.3))
