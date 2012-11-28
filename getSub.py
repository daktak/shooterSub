#!/usr/bin/python2
# grab subs for all videos without subs
# set videoDir corrcetly
import os
import stat
from time import gmtime, strftime

movieExt = ['avi','mp4','wmv']
subExt = ['srt','ass']
videoDir = "/pub/video/tv_shows"
shooterGrabber = "/usr/local/bin/shooterSub.py"

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
for (basepath, children) in walktree(videoDir,False):
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
                exitCode = os.system(shooterGrabber + " \"" + item +"\"");
		#exitCode = os.system("ls")
		if (exitCode == 0):
		    print varDate,"[\033[1;32mOK\033[0m]",item
		else:
		    print varDate,"[\033[1;31mFail\033[0m]",item

 #iconv -f big5 -t utf-8 Missing\ \(2012\)\ -\ s01e06\ -\ A\ Busy\ Solitude.srt  -cs > ~/out.txt

