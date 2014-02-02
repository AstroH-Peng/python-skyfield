"""Compare the output of Skyfield with the routines from NOVAS for keplerian orbiting bodies"""

from skyfield import coordinates
import skyfield.keplerianlib
from skyfield.keplerianlib import KeplerianOrbit, ICRCoordinates
import de421

from ..timelib import JulianDate, julian_date

def test_semimajorAxisToOrbitalPeriod():
    assert skyfield.keplerianlib.semimajorAxisToOrbitalPeriod(1) == 1
    assert skyfield.keplerianlib.semimajorAxisToOrbitalPeriod(1.523679) == 1.8807896358663763
    assert skyfield.keplerianlib.semimajorAxisToOrbitalPeriod(4.27371348392) == 8.835031547398543

def test_orbitalPeriodToSemimajorAxis():
    assert skyfield.keplerianlib.orbitalPeriodToSemimajorAxis(1) == 1
    assert skyfield.keplerianlib.orbitalPeriodToSemimajorAxis(1.8807896358663763) == 1.523679
    assert skyfield.keplerianlib.orbitalPeriodToSemimajorAxis(8.835031547398543) == 4.27371348392

def test_convergeEccentricAnomaly():
    test = skyfield.keplerianlib.convergeEccentricAnomaly(
        hoyle_8077['mean_anomaly'],
        hoyle_8077['eccentricity'],
        15
    )
    assert test == hoyle_8077['eccentric_anomaly']

def test_instantiate_8077_hoyle():
    hoyle = KeplerianOrbit( hoyle_8077['semimajor_axis'],
                            hoyle_8077['eccentricity'],
                            hoyle_8077['inclination'],
                            hoyle_8077['longitude_ascending'],
                            hoyle_8077['argument_perihelion'],
                            hoyle_8077['mean_anomaly'],
                            hoyle_8077['epoch'])

    assert hoyle != None

def test_instantiate_coordinates():
    coords = ICRCoordinates(x=500.25, y=10.76, z=0.1125)

    assert coords != None

def test_coordinatesEquivalence():
    coords_the_first = ICRCoordinates(x=500.25, y=10.76, z=0.1125)
    coords_the_second = ICRCoordinates(x=500.25, y=10.76, z=0.1125)

    assert coords_the_first.equalTo(coords_the_second)

"""
 data gotten from Horizons
date: 2456517.500000000 = A.D. 2013-Aug-13 00:00:00.0000 (CT)
expected coords (AU) 2.421251132790093E+00 -1.918893156489506E+00 -9.813409585464707E-02

 Horizon Params
Ephemeris Type [change] :   VECTORS
Target Body [change] :  Asteroid 8077 Hoyle (1986 AW2)
Coordinate Origin [change] :    Solar System Barycenter (SSB) [500@0]
Time Span [change] :    Start=2013-08-13, Stop=2013-09-12, Step=1 d
Table Settings [change] :   defaults
Display/Output [change] :   default (formatted HTML)

EPOCH=  2453995.5 ! 2006-Sep-17.00 (CT)          Residual RMS= .43359
   EC= .2110946491840378   QR= 2.077692130214496   TP= 2454360.1855338747
   OM= 135.855972529608    W=  34.4378477722205    IN= 17.25814783060462
   A= 2.633639292806857    MA= 275.9015153135912   ADIST= 3.189586455399217
   PER= 4.27408            N= .230605479           ANGMOM= .027287332
   DAN= 2.14316            DDN= 3.04671            L= 169.07331
   B= 9.658454799999999    MOID= 1.10581994        TP= 2007-Sep-16.6855338747

"""

hoyle_8077 = {
    'semimajor_axis' :  2.633639292806857,
    'eccentricity' : .2110946491840378,
    'inclination' : 17.25814783060462,
    'longitude_ascending' : 135.855972529608,
    'argument_perihelion' : 34.4378477722205,
    'mean_anomaly' : 275.9015153135912,
    'eccentric_anomaly' : 4.60549996242,
    'epoch' : JulianDate(tt=julian_date(2007, 9, 16, 0)),
}


def test_get_8077_hoyle_ecliptic_on_dev_sprint_day_2():
    hoyle = KeplerianOrbit( hoyle_8077['semimajor_axis'],
                            hoyle_8077['eccentricity'],
                            hoyle_8077['inclination'],
                            hoyle_8077['longitude_ascending'],
                            hoyle_8077['argument_perihelion'],
                            hoyle_8077['mean_anomaly'],
                            hoyle_8077['epoch'])

    date = JulianDate(tt=julian_date(2013, 8, 13, 0))

    expected = ICRCoordinates(2.421251132790093, -1.918893156489506, -0.09813409585464707)

    test = hoyle.getECLCoordinatesOnJulianDate(date)

    #print test
    assert test.equalTo(expected)
