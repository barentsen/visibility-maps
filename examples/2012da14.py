import sys
sys.path.append("../")
import logging
import visibility   
from multiprocessing import Pool

# Ephemerides from NASA JPL Horizons
ephemerides = [{'time':"18:00", 'ra':168.95103, 'dec':-57.37510},
         {'time':"18:10", 'ra':169.78703, 'dec':-53.37342},
         {'time':"18:20", 'ra':170.55989, 'dec':-48.85117},
         {'time':"18:30", 'ra':171.27845, 'dec':-43.75373},
         {'time':"18:40", 'ra':171.95049, 'dec':-38.04079},
         {'time':"18:50", 'ra':172.58296, 'dec':-31.70096},
         {'time':"19:00", 'ra':173.18216, 'dec':-24.76953},
         {'time':"19:10", 'ra':173.75385, 'dec':-17.34398},
         {'time':"19:20", 'ra':174.30332, 'dec':-9.58889},
         {'time':"19:30", 'ra':174.83543, 'dec':-1.72174},
         {'time':"19:40", 'ra':175.35460, 'dec':6.02047},
         {'time':"19:50", 'ra':175.86475, 'dec':13.42266},
         {'time':"20:00", 'ra':176.36935, 'dec':20.32413},
         {'time':"20:10", 'ra':176.87140, 'dec':26.63149},
         {'time':"20:20", 'ra':177.37345, 'dec':32.31286},
         {'time':"20:30", 'ra':177.87769, 'dec':37.38200},
         {'time':"20:40", 'ra':178.38597, 'dec':41.88063},
         {'time':"20:50", 'ra':178.89990, 'dec':45.86412},
         {'time':"21:00", 'ra':179.42087, 'dec':49.39164},
         {'time':"21:10", 'ra':179.95012, 'dec':52.52042},
         {'time':"21:20", 'ra':180.48875, 'dec':55.30278},
         {'time':"21:30", 'ra':181.03777, 'dec':57.78508}]

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