#!/usr/bin/python2
# grab subs for all videos without subs
# set videoDir corrcetly
import os
import sys
import stat
from time import gmtime, strftime
from configobj import ConfigObj
try: 
    confFile = sys.argv[1]
except :
    confFile = '/etc/shootersub/shooterSub.ini'
config = ConfigObj(confFile)

movieExt = config['Options']['movieExt']
subExt = config['Options']['subExt'] 
videoDir = config['General']['videoDir']
shooterGrabber =  config['General']['shooterGrabber']
fallback = config['Options']['fallback']
fallbackExec = config['Options']['fallbackExec']

def walktree (top = ".", depthfirst = True):
    names = os.listdir(top)
    if not depthfirst:
        yield top, names
    for name in names:
        try:
            st = os.lstat(os.path.join(top, name))
        except os.error:
            continue
        if stat.S_ISDIR(st.st_mode):
            for (newtop, children) in walktree (os.path.join(top, name), depthfirst):
                yield newtop, children
    if depthfirst:
        yield top, names

L = []
for videoir in videoDir:
    print videoir
    for (basepath, children) in walktree(videoir,False):
        for child in children:
            #print os.path.join(basepath, child)
            #print child
            L.append(os.path.join(basepath, child))

found = False
for item in L:
    for movext in movieExt:
        if (item.endswith(movext)):
            found = False
            for sub in L:
                for subex in subExt:
                    if (item.rstrip(movext)==sub.rstrip(subex)):
                        #print sub
                        found = True
            #print found
            if (not found):            
	        varDate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                exitCode = os.system(shooterGrabber + " \"" + item +"\"")
		#exitCode = os.system("ls")
		if (exitCode == 0):
		    print varDate,"[\033[1;32mOK\033[0m]",item
		else:
		    if 'True' in fallback:
		        exitCode = os.system(fallbackExec  + " \"" + item +"\"")
		    else:
		        print varDate,"[\033[1;31mFail\033[0m]",item

 #iconv -f big5 -t utf-8 output.srt  -cs > ~/out.txt

