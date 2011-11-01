#!/usr/bin/env python

""" A Class to handle MOM4 outputs
"""


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
        super(MOM4p1, self).__init__(urlpath)
        self.name = 'MOM4p1'

    def get_data(self, l0, j0, i0):
        return ma.masked_equal(
                self.field.array[l0:l0 + 2, :, j0:j0 + 2, i0:i0 + 2],
                self.field.missing_value)

