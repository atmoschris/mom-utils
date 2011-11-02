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


class Modelo_from_nc(UserDict):
    """
    """
    def __init__(self,ncfpath):
        """
        """
        import netCDF4
        self.dataset = netCDF4.Dataset(ncfpath)
        self.data = {}
    def keys(self):
        keys = self.data.keys()
	for k in self.dataset.variables.keys():
	    if k not in keys:
	        keys.append(k)
        return keys
    def __getitem__(self,index):
        """
        """
        if index in self.data.keys():
            return self.data[index]
        if index in self.data.keys():
            return self.data[index]
        field = self.dataset.variables[index]
        if (index,) == field.dimensions:
            self.data[index] = ma.array(field[:])
            self.data[index].units = field.units
            return self.data[index]
        else:
            data = ma.masked_values(field[:], field.missing_value)
            data.units = field.units
            data.long_name = field.long_name
            data.dimensions = field.dimensions
            return data
        #    return self.data[index]
        return

class Modelo_from_nca(UserDict):
    """
    """
    def __init__(self,ncfpath):
        """
        """
        self.data = {}
        self.dataset = []
        for ncf in ncfpath:
            self.dataset.append(Modelo_from_nc(ncf))
        #
        self._build_time()
        return
    def _build_time(self):
        time = numpy.array([])
        mask = numpy.array([], dtype='bool')
	for d in self.dataset:
            time = numpy.append(time, d['time'].data)
            mask = numpy.append(mask, ma.getmaskarray(d['time']))
	self.data['time'] = ma.masked_array(time,mask)
    def keys(self):
        keys = self.data.keys()
	for k in self.dataset[0].keys():
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

        dims = self.dataset[0].dataset.variables[index].dimensions
        if 'time' in dims:
            if 'time' == dims[0]
            data = numpy.array([])
            mask = numpy.array([], dtype='bool')
            for d in self.dataset:
                time = numpy.append(data, d[index].data)
                mask = numpy.append(mask, ma.getmaskarray(d[index]))
            return = ma.masked_array(time,mask)
        else:
	    return self.dataset[0][index]


#ncfpath = ["/stornext/grupos/ocean/simulations/exp030/dataout/ic200701/ocean/CGCM/20070101.ocean_transport.nc", "/stornext/grupos/ocean/simulations/exp030/dataout/ic200701/ocean/CGCM/20080101.ocean_transport.nc"]
#reload(mom4)
x = Modelo_from_nca(ncfpath)
x.keys()
#x['xu_ocean']
#x['ty_trans']

##if __name__ == '__main__':
#urlpath="http://opendap.ccst.inpe.br/Models/CGCM2.1/exp030/20070101.ocean_transport.nc"
#from pydap.client import open_url
#dataset = open_url(urlpath)
#import mom4
#reload(mom4)
#x = mom4.Modelo_from_dap(urlpath = urlpath)
#print dir(x)

