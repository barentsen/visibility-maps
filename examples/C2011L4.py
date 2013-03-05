import sys
sys.path.append("../")
import logging
import visibility
import ephem
import datetime
from multiprocessing import Pool

# xephem line obtained from MPC
target = 'C/2011 L4 (PANSTARRS),h,03/10.1696/2013,84.2072,65.6658,333.6517,1.000028,0.301542,2000,5.5,4.0'

def do_plot(date):
    logging.info(date)

    step = 0.2
    m = visibility.Map(lonstep=step, latstep=step)
    m.set_target_xephem(target)
    m.render(date)

    m.figure.text(.03, .93, 'Visibility of comet Pan-STARRS', fontsize=22, ha='left')
    m.figure.text(.03, .87, '%d %s at %s UTC' % (
                                date.day, 
                                date.strftime('%B %Y'), 
                                date.strftime('%H:%M'))
                            , fontsize=22, ha='left')
    m.figure.savefig('tmp/C2011L4-%s.png' % date.strftime('%Y%m%dT%H%M'), dpi=150)


if __name__ == '__main__':
    dates = []
    stepsize = datetime.timedelta(hours=0.5)
    mydate = datetime.datetime(2013, 3, 5)
    for i in range(24*60):
        dates.append( mydate )
        mydate += stepsize

    p = Pool(processes=4)
    p.map(do_plot, dates)

    #do_plot(mydate)
