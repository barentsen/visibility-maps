import sys
sys.path.append("../")
import logging
import visibility
import ephem
from multiprocessing import Pool


mydate = "2013/03/15 22:00:00"

target = 'C/2011 L4 (PANSTARRS),h,03/10.1696/2013,84.2072,65.6658,333.6517,1.000028,0.301542,2000,5.5,4.0'
m = visibility.Map()
m.set_target_xephem(target)
m.render(mydate)
m.figure.savefig('test.png')


"""

def do_plot(eph):
    logging.info(eph)
    # Target
    mydate = "2013/02/15 %s:00" % eph['time']
    ra = eph['ra']
    dec = eph['dec']
    # Coordinates of map corners
    lon1, lon2 = -170, 190
    lat1, lat2 = -57, 74
    # Create and save map
    m = visibility.Map(mydate, ra, dec, lon1, lon2, lat1, lat2, 0.2, 0.2)
    m.render()
    m.figure.text(.5, .93, 'Visibility of 2012 DA14 at %s UTC' % eph['time'], fontsize=26, ha='center')
    m.figure.text(.5, .88, '15 February 2013', fontsize=18, ha='center')
    m.figure.savefig('2012DA14-%s.png' % eph['time'])


if __name__ == '__main__':
    p = Pool(processes=8)
    p.map(do_plot, ephemerides)

"""