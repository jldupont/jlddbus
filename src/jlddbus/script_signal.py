"""
    Created on 2015-02-28
    @author: jldupont
"""
import os
import logging

import dbus.service

from twisted.internet import glib2reactor
glib2reactor.install()

from twisted.internet import reactor
from twisted.internet import stdio
from twisted.protocols import basic

from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)


class SystemicalObject(dbus.service.Object):
    def __init__(self, conn, object_path):
        dbus.service.Object.__init__(self, conn, object_path)

    @dbus.service.signal('com.systemical.signals')
    def emit_signal(self, message):
        """
        signal sender=:1.208 -> dest=(null destination) serial=20 path=/test; interface=com.systemical.signals; member=emit_signal
           string "{"usn": " uuid:02DA8AC3-07AE-9140-ED8D-EEBA2A31B277", "nt": " uuid:02DA8AC3-07AE-9140-ED8D-EEBA2A31B277", "location": " http://192.168.1.1/HNAP1/", "server": " POSIX, UPnP/1.0 linux/5.10.56.51"}"
        """

     

class Main(basic.LineReceiver):
    
    def __init__(self, bus, dobj):
        self.bus = bus
        self.dobj = dobj
    
    delimiter = os.linesep
    
    def connectionMade(self):
        logging.info("Connection established")
        
    def lineReceived(self, line):
        logging.info("Line:\n %s" % repr(line))
        self.dobj.emit_signal(line)

def run(path=None):
    """
    Entry Point
    """
    
    bus = dbus.SystemBus()
    
    dobj = SystemicalObject(bus, path)
    
    ppid=os.getppid()
    logging.info("Process pid: %s" % os.getpid())
    logging.info("Parent pid : %s" % ppid)
    logging.info("Starting loop...")
    
    stdio.StandardIO(Main(bus, dobj))
    reactor.run()
    
    
    '''
    while True:
        
        ### protection against broken pipe
        if os.getppid()!=ppid:
            logging.warning("Parent process terminated... exiting")
            break
        
        iline=sys.stdin.readline().strip()
        
        try:
            jdict = json.loads(iline)
        except:
            logging.warning("Can't JSON decode: %s" % repr(iline))
            continue
        
        logging.info("Received: %s" % repr(jdict))
        #dobj.emit_signal(json.dumps(jdict))
    '''
     
#
#
#