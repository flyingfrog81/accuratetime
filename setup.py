from distutils.core import setup

setup(name = 'accuratetime',
        version = '0.5',
        author = 'Marco Bartolini',
        author_email = 'marco.bartolini@gmail.com',
        url = "https://github.com/flyingfrog81/accuratetime",
        download_url = "https://github.com/flyingfrog81/accurate_time/zipball/master",
        license = "gpl",
        description = "utility for extending python datetime precision",
        py_modules = ['accuratetime'],
        classifiers = [
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Natural Language :: English",
            "Programming Language :: Python",
            ],
        long_description = """
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

        """,
        )
