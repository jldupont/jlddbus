"""
    Created on 2015-02-28
    @author: jldupont
"""
import os
import logging


from signal import signal, SIGPIPE, SIG_DFL 
signal(SIGPIPE,SIG_DFL) 



import dbus.service

from twisted.internet import glib2reactor
glib2reactor.install()


from twisted.internet import reactor
from twisted.internet import stdio
from twisted.protocols import basic
from twisted.internet.task import LoopingCall


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
    
    def __init__(self, bus, dobj, debug=False):
        self.bus = bus
        self.dobj = dobj
        self.debug = debug
    
    delimiter = os.linesep
    
    def connectionMade(self):
        if self.debug:
            logging.info("Connection established")
        
    def lineReceived(self, line):
        if self.debug:
            logging.info("Line:\n %s" % repr(line))
        self.dobj.emit_signal(line)


    
def watch_dog_task(start_ppid, debug=False):
    """
    If our parent exited there is no use pursuing
    """
    current_ppid = os.getppid()
    if current_ppid!=start_ppid:
        logging.warning("Parent exited...")
        reactor.stop()



def run(path=None, debug=False):
    """
    Entry Point
    """
    
    bus = dbus.SystemBus()
    
    dobj = SystemicalObject(bus, path)
    
    ppid=os.getppid()
    
    if debug:
        logging.info("Process pid: %s" % os.getpid())
        logging.info("Parent pid : %s" % ppid)
        logging.info("Starting loop...")
    
    ##
    ## Every 5 seconds check if we need to exit
    ##
    lc = LoopingCall(lambda:watch_dog_task(ppid, debug=debug))
    lc.start(5)
    
    stdio.StandardIO(Main(bus, dobj, debug=debug))
    reactor.run()
    
     
#
#
#