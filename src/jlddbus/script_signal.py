"""
    Created on 2015-02-28
    @author: jldupont
"""
import os
import sys
import logging
import json



def run(*p, **k):
    """
    Entry Point
    """
    
    ppid=os.getppid()
    logging.info("Process pid: %s" % os.getpid())
    logging.info("Parent pid : %s" % ppid)
    logging.info("Starting loop...")
    
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