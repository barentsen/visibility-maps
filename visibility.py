"""
Plot a global visibility map of a celestial object
Author: Geert Barentsen
"""
import matplotlib as mpl
mpl.use('Agg')
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import ephem


class Map():
    """Computes a visibility map"""

    def __init__(self, lon1=-170., lon2=190., 
                 lat1=-57., lat2=74., lonstep=1.0, latstep=1.0):
        """
        Arguments
        date: Time (UTC)
        ra/dec: Equatorial coordinates of the celestial object (degrees)
        lon1/lon2: Longitudes at the left and right edges of the map (degrees east)
        lat1/lat2: Latitudes at the bottom and top edges of the map (degrees north)
        """
        self.lon1, self.lon2 = lon1, lon2
        self.lat1, self.lat2 = lat1, lat2
        self.latitudes = np.arange(lat1, lat2+latstep, latstep)
        self.longitudes = np.arange(lon1, lon2+lonstep, lonstep)

    def set_target(self, ra, dec):
        self.target = ephem.FixedBody()
        self.target._ra = ephem.degrees('%s' % ra)
        self.target._dec = ephem.degrees('%s' % dec)

    def set_target_xephem(self, xephem):
        self.target = ephem.readdb(xephem)

    def _compute_elevations(self, date):
        """Compute the object and the solar elevation across Earth using PyEphem"""
        # Sun Pyephem object
        sun = ephem.Sun()

        result = [] # list containing radiant altitudes across the world (or NaN if daylight)
        for lat in self.latitudes:
            for lon in self.longitudes:
                # Create a PyEphem "Observer" object at the given lon/lat
                observer = ephem.Observer()
                observer.lat = ephem.degrees('%s' % lat)
                observer.long = ephem.degrees('%s' % lon)
                observer.date = date
                
                # Compute target and solar elevation
                self.target.compute(observer)
                target_alt = np.degrees(self.target.alt) 
                sun.compute(observer)
                sun_alt = np.degrees(sun.alt) 
                
                if sun_alt > -6 or target_alt < 0:
                    result.append( np.NaN )
                else:
                    result.append( target_alt )

        # Return the result as a matrix
        return np.array(result).reshape(len(self.latitudes), 
                                        len(self.longitudes))

    def render(self, date, mode='web'):
        elevations = self._compute_elevations(date)

        """ Create the plot """
        self.figure = plt.figure(figsize=(8.485, 6))
        self.figure.subplots_adjust(0.01, 0.00, 0.99, 0.95, 
                                    hspace=0.0, wspace=0.0)

        # Show earth with Mercator projection
        ax = Basemap(projection='merc', 
                    llcrnrlon=self.lon1, llcrnrlat=self.lat1, 
                    urcrnrlon=self.lon2, urcrnrlat=self.lat2, 
                    resolution="c", fix_aspect=False)
        ax.drawcoastlines()


        if mode == 'pub':
            cdict = {'red'  :    ((0., .75, .75), (1., 0.05, 0.05)), 
                     'green':  ((0., .75, .75), (1., 0.05, 0.05)), 
                     'blue' :  ((0., .75, .75), (1., 0.05, 0.05))}
        else:
            cdict = {'red'  :  ((0., 1., 1.), (1., .1, 0.)), 
                 'green':  ((0., 1., 1.), (1., 1., 1.)), 
                 'blue' :  ((0., 0., 0.), (1., 0., 0.))}

        my_cmap = mpl.colors.LinearSegmentedColormap('my_colormap', cdict, 1024)
        im = ax.imshow(elevations, cmap=my_cmap, vmin=0, vmax=90)
                
        cb = self.figure.colorbar(im, orientation='horizontal', pad=0.02, shrink=0.95, 
                            ticks=[0,30,60,90], aspect=50, format=u'%.0f\N{DEGREE SIGN}')
        cb.ax.set_xlabel('Elevation above the horizon', fontsize=18)
        cl = plt.getp(cb.ax, 'xmajorticklabels')
        plt.setp(cl, fontsize=14)



if __name__ == '__main__':
    """Example"""

    # Target
    mydate = "2013/02/15 19:00:00"
    ra = 173.18216
    dec = -24.76953
    # Create and save map
    m = Map()
    m.set_target(ra, dec)
    m.render(mydate)
    m.figure.text(.5, .93, 'Visibility of 2012 DA14 at 19h00 UTC', fontsize=26, ha='center')
    m.figure.text(.5, .88, '15 February 2013', fontsize=18, ha='center')
    m.figure.savefig('tmp/19h00.png')
