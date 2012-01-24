# coding=utf-8

#
#
#    Copyright (C) 2012  Marco Bartolini, marco.bartolini@gmail.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
ACCURATE TIME
=============

This module defines an AccurateTime object for storing arbitrary precision
floating point posix time while keeping the same information as a standard
datetime object, keeping consistency between the two

INSTALLATION
============

You are free to clone the public git repo as::

    $ git clone git://github.com/flyingfrog81/accuratetime.git
    $ cd accuratetime
    $ python setup.py install

Or you can install using PyPI as::

    $ pip install accuratetime

USAGE
=====

    >>> import accuratetime
    >>> import time
    >>> t_zero = accuratetime.now()
    >>> time.sleep(3.5)
    >>> t_uno = accuratetime.now()
    >>> t_delta_datetime = t_uno.datetime - t_zero.datetime
    >>> t_zero.datetime += t_delta_datetime
    >>> t_zero.accurate_posix == t_uno.accurate_posix
    True
    >>> t_uno = accuratetime.now()
    >>> t_delta_posix = t_uno.accurate_posix - t_zero.accurate_posix
    >>> t_zero.accurate_posix += t_delta_posix
    >>> t_zero.datetime == t_uno.datetime
    True

@author: Marco Bartolini
@contact: marco.bartolini@gmail.com
@version: 0.5
"""

import datetime
import time
#from functools import total_ordering #Python2.7

#@total_ordering
class AccurateTime(object):
    '''
    Class for storing a POSIX time with arbitrary floating point precision.
    It can return datetime objects as well as posix time and the values are
    kept synchronized between each other.
    In order to keep consisency between datetime object and posix time
    information, changes must be made using I{datetime} and I{accurate_posix}
    public attributes.
    '''
    def __init__(self, ptime=0):
        """
        Constructor. Module function can be used for type conversion.
        @type ptime: float
        @param ptime: seconds since Epoch
        """
        self._datetime = datetime.datetime.fromtimestamp(ptime)
        self._accurate_posix = float(ptime)

    @property
    def accurate_posix(self):
        """
        The posix time representation of the information. Stored in arbitrary
        precision.
        """
        return self._accurate_posix

    @accurate_posix.setter
    def accurate_posix(self, new_val):
        self._accurate_posix = new_val
        self._datetime = datetime.datetime.fromtimestamp(new_val)

    @property
    def datetime(self):
        """
        The datetime representation of the information. You can modify this
        attribute using datetime python utilities and relative changes will be reflected
        in the accurate_posix attribute.
        """
        return self._datetime

    @datetime.setter
    def datetime(self, new_val):
        td = new_val - self._datetime
        self._datetime = new_val
        self._accurate_posix += td.total_seconds()

    def microseconds(self):
        """
        Gives the exact microsecond of the represented time
        @return: a floating point number representing microseconds
        """
        return self._accurate_posix % 1 * 1000000

    def __add__(self, other):
        """
        Addition operator. 
        @type other: a datetime.timedelta instance or a numeric type
        @param other: a time difference
        @return: a new L{AccurateTime} instance
        @raise TypeError: if values cannot be summed up
        """
        try:
            return from_datetime(self._datetime + other)
        except TypeError:
            try:
                return from_ptime(self._accurate_posix + other)
            except TypeError:
                raise TypeError("unsupported operand type(s) for +: 'AccurateTime' and " + type(other))

    def __sub__(self, other):
        """
        Subtraction operator. 
        @type other: a datetime.timedelta instance or a numeric type
        @param other: a time difference
        @return: a new L{AccurateTime} instance
        @raise TypeError: if values cannot be subtracted from each other
        """
        try:
            return from_datetime(self._datetime - other)
        except TypeError:
            try:
                return from_ptime(self._accurate_posix - other)
            except TypeError:
                raise TypeError("unsupported operand type(s) for +: 'AccurateTime' and '" + str(type(other)) + "'")

def from_datetime(dt):
    """
    Creates a new AccurateTime object with given informations
    @type dt: datetime.datetime
    @param dt: the datetime object to be parsed
    @return: the AccurateTime instance
    """
    return AccurateTime(time.mktime(dt.timetuple()))

def from_ptime(pt):
    """
    Creates a new AccurateTime object with given informations
    @type pt: float
    @param pt: posix time as a floating point number
    @return: the AccurateTime instance
    """
    return AccurateTime(pt)

def now():
    """
    Creates a new AccurateTime object representing the I{now} time
    @return: the AccurateTime instance
    """
    return AccurateTime(time.mktime(datetime.datetime.now().timetuple()))
