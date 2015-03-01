"""
    Created on 2012-01-19
    @author: jldupont
"""

try:
    import argparse #@UnusedImport
except:
    raise Exception("* package 'argparse' is necessary - get it from Pypi\n")

try:
    import dbus #@UnusedImport
except:
    raise Exception("* package 'python-dbus' is necessary - apt-get install it\n")


try:
    import gobject #@UnusedImport
except:
    raise Exception("* package 'python-gobject' is necessary - apt-get install it\n")
