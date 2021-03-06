#!/usr/bin/env python

"""
Trying to channel debug output

debug levels (examples):
0 - non-repeating output (starting up, shutting down), error messages
1 - function return values
2 - lower debug data, function input values, intermediate info...
"""

dlevels = { "PlexNMT": 2, \
            "PlexAPI"    : 2, \
            "WebServer"  : 2, \
            "XMLConverter" : 2, \
            "Settings"   : 2, \
            "Localize"   : 0, \
          }


import time
from lxml import etree

#try:
#    import xml.etree.cElementTree as etree
#except ImportError:
#    import xml.etree.ElementTree as etree



g_logfile = ''
g_loglevel = 0

def dinit(src, param, newlog=False):    
    if 'LogFile' in param:
        global g_logfile
        g_logfile = param['LogFile']
        
    if 'LogLevel' in param:
        global g_loglevel
        g_loglevel = { "Normal": 0, "High": 2, "Off": -1 }.get(param['LogLevel'], 0)
    
    if not g_loglevel==-1 and not g_logfile=='' and newlog:
        f = open(g_logfile, 'w')
        f.close()
        
    dprint(src, 0, "started: {0}", time.strftime("%H:%M:%S"))



def dprint(src, dlevel, *args):
    logToTerminal = not (src in dlevels) or dlevel <= dlevels[src]
    logToFile = not g_loglevel==-1 and not g_logfile=='' and dlevel <= g_loglevel
    
    if logToTerminal or logToFile:
        asc_args = list(args)
        
        for i,arg in enumerate(asc_args):
            if isinstance(asc_args[i], str):
                asc_args[i] = asc_args[i].decode('utf-8', 'replace')  # convert as utf-8 just in case
            if isinstance(asc_args[i], unicode):
                asc_args[i] = asc_args[i].encode('ascii', 'replace')  # back to ascii
        
        # print to file (if filename defined)
        if logToFile:
            f = open(g_logfile, 'a')
            f.write(time.strftime("%H:%M:%S "))
            if len(asc_args)==0:
                f.write(src+":\n")
            elif len(asc_args)==1:
                f.write(src+": "+asc_args[0]+"\n")
            else:
                f.write(src+": "+asc_args[0].format(*asc_args[1:])+"\n")
            f.close()
        
        # print to terminal window
        if logToTerminal:
            print(time.strftime("%H:%M:%S")),
            if len(asc_args)==0:
                print src+":"
            elif len(asc_args)==1:
                print src+": "+asc_args[0]
            else:
                print src+": "+asc_args[0].format(*asc_args[1:])



"""
# XML in-place prettyprint formatter
# Source: http://stackoverflow.com/questions/749796/pretty-printing-xml-in-python
"""
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def prettyXML(XML):
    if g_loglevel>0:
        indent(XML.getroot())
    return(etree.tostring(XML.getroot()))



if __name__=="__main__":
    dinit('Debug', {'LogFile':'Debug.log'}, True)  # True -> new file
    dinit('unknown', {'Logfile':'Debug.log'})  # False/Dflt -> append to file
    
    dprint('unknown', 0, "debugging {0}", __name__)
    dprint('unknown', 1, "level 1")
    
    dprint('PlexNMT', 0, "debugging {0}", 'PlexNMT')
    dprint('PlexNMT', 1, "level")
