#!/usr/bin/env python

""" A Class to handle MOM4 outputs
"""

from pydap.client import open_url

class Model(object):

    def __init__(self, urlpath):
        self.data = open_url(urlpath)
        self._field = None

    @property
    def field(self):
        return self._field

    @field.setter
    def field(self, field):
        self._field = self.data[field]

    @property
    def lon(self):
        LON = self.field.dimensions[-1]
        return self.data[LON][:]

    @property
    def lat(self):
        LAT = self.field.dimensions[-2]
        return self.data[LAT][:]

    @property
    def depth(self):
        DEPTH = self.field.dimensions[-3]
        return self.data[DEPTH][:]

    @property
    def time(self):
        TIME = self.field.dimensions[-4]
        return [(v, self.data[TIME].units) for v in self.data[TIME][:]]


class MOM4p1(Model):

    def __init__(self, urlpath):
        print urlpath
        super(MOM4p1, self).__init__(urlpath)
        self.name = 'MOM4p1'

    def get_data(self, l0, j0, i0):
        return ma.masked_equal(
                self.field.array[l0:l0 + 2, :, j0:j0 + 2, i0:i0 + 2],
                self.field.missing_value)

from UserDict import UserDict
import numpy
from numpy import ma

class Modelo_from_dap(UserDict):
    """
    """
    def __init__(self,urlpath):
        """
        """
        from pydap.client import open_url
        self.data = {}

        self.dataset = open_url(urlpath)
        ## Dictionary with the reference data for the model
        ##print "Available: ",dataset_model.keys()
        #for v in ['time','xt_ocean','yt_ocean','st_ocean']:
        #    self.data[v] = ma.array(self.dataset[v][:])
        ## Adjust the grid to the regular [-180:180]
        #self.data['xt_ocean'][self.data['xt_ocean']<-180] = self.da
        return

    def keys(self):
        keys = self.data.keys()
	for k in self.dataset.keys():
	    if k not in keys:
	        keys.append(k)
        return keys

    def __getitem__(self,index):
        """
        """
	if index in self.data.keys():
            return self.data[index]

        if index not in self.keys():
	    return

	field = getattr(self.dataset, index)
	if (index,) == field.dimensions:
	    self.data[index] = ma.array(field[:])
	    self.data[index].attributes = field.attributes
	    return self.data[index]
	else:
	    # Not sure the best way to do it
	    # To be transparent I should get the data as an array
	    # But there is always the risk to bring eveything by mistake
	    self.data[index] = ma.masked_values(field[index][:],field.missing_value)
	    #self.data[index].attributes = field.attributes
	    print dir(field[index])


	return field


#if __name__ == '__main__':
urlpath="http://opendap.ccst.inpe.br/Models/CGCM2.1/exp030/20070101.ocean_transport.nc"
from pydap.client import open_url
dataset = open_url(urlpath)
import mom4
reload(mom4)
x = mom4.Modelo_from_dap(urlpath = urlpath)
print dir(x)




