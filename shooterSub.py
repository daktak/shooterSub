#!/usr/bin/python2
# based on xbmc-addons-chinese
import sys
import os
#import xbmc
import string
import tempfile,urllib2,urllib,struct,gzip,StringIO,md5,xml.dom.minidom
from configobj import ConfigObj
import chardet
from guess_language import guessLanguageTag

confFile = '/etc/shootersub/shooterSub.ini'
config = ConfigObj(confFile)
hasPath = True 
pathName = '';
destCode = config['Options']['encoding'] 
no_sub_file = config['General']['no_sub_file']
validLang = config['Options']['validLangs']
url = config['Options']['url']

#movieFullPath = "/pub/video/test.avi"

if (len(sys.argv) > 1):
    movieFullPath = sys.argv[1]
else:
    #print "Please specify filename\t[\033[1;31mFail\033[0m]\n"
    sys.exit(1)
try:
    file=open(movieFullPath,"rb")
except IOError:
  #print "File could not be opened\t[\033[1;31mFail\033[0m]\n"
  sys.exit(2)

BlockSize = 4096
NumOfSegments = 4

fileLength = os.path.getsize(movieFullPath)
offset = []
offset.append(BlockSize)
offset.append(fileLength / 3 * 2)
offset.append(fileLength / 3)
offset.append(fileLength - 8192)

buff = []
strHash = ''

for i in range(0,NumOfSegments):
    file.seek(offset[i])
    buff = file.read(BlockSize)
    if (len(strHash) > 0):
        strHash += ";"
    m = md5.new()
    m.update(buff)
    strHash += m.hexdigest()

#print strHash

file.close()

Boundary='----------------------------767a02e50d82'
user_agent = 'SPlayer Build 2437'
#580
ContentType = "multipart/form-data; boundary=----------------------------767a02e50d82"
dataValue = 'Content-Disposition: form-data; name='
headers = { 'User-Agent' : user_agent,
            'Content-Type' : ContentType,
            'Connection' : 'Keep-Alive',
            'Expect' : '100-continue'}

realData = '--' + Boundary + '\r\n' + dataValue + "\"pathinfo\"\r\n\r\n" + movieFullPath + '\r\n'
realData += '--' + Boundary + '\r\n' + dataValue + "\"filehash\"\r\n\r\n" + strHash + '\r\n'
realData += '--' + Boundary + '--\r\n'

req = urllib2.Request(url, realData, headers)
response = urllib2.urlopen(req)
the_page = response.read()
#print the_page
#temp = open('/tmp/chs','wb')
#temp.write(the_page)
#temp.close()
if(len(the_page) > 2):
    NumOfSub = ord(the_page[:1])
    fileLen = 0
    nowPos = 1
    for i in range(0, NumOfSub):
        #print i
        packLen = struct.unpack('!L',the_page[nowPos:nowPos+4])
        nowPos += 4
        desLen = struct.unpack('!L',the_page[nowPos:nowPos+4])
        nowPos += desLen[0] + 4
        subPack = ord(the_page[nowPos+4:nowPos+5])
        nowPos += 9
        extLen = struct.unpack('!L',the_page[nowPos:nowPos+4])
        nowPos += 4
        fileExt = the_page[nowPos:nowPos+extLen[0]]
        nowPos += extLen[0]
        #print fileExt
        fileLen = struct.unpack('!L',the_page[nowPos:nowPos+4])
        nowPos += 4
        #fileName = movieFullPath[:-4] + '.chs' + str(i) +'.' + fileExt
        fileName = movieFullPath[:-4] + '.' + fileExt
        #print fileName
        org_file = the_page[nowPos:nowPos+fileLen[0]]
        if(hasPath == 'True'):
            zip_file = open(os.path.join(pathName,os.path.basename(fileName)),'wb')
        else:
            zip_file = open(fileName,'wb')

        if ((ord(org_file[0]) == 31) and (ord(org_file[1]) == 139) and (ord(org_file[2]) == 8)) :
            compressedstream = StringIO.StringIO(org_file)
            f = gzip.GzipFile(fileobj=compressedstream)
            data = f.read()
            if((ord(data[0]) == 255) and (ord(data[1]) == 254)):
                temp_data = unicode(data[2:],'utf-16')
                zip_file.write(temp_data.encode(destCode, 'ignore'))
            else:
                zip_file.write(data)

        else:
            data = the_page[nowPos:nowPos+fileLen[0]]
            if((ord(data[0]) == 255) and (ord(data[1]) == 254)):
                temp_data = unicode(data[2:],'utf-16')
                zip_file.write(temp_data.encode(destCode, 'ignore'))
            else:
                zip_file.write(data)

        zip_file.close()
        nowPos += fileLen[0]
        #print "\t[\033[1;32mSuccess\033[0m]\n" 
else:
    #print "Error: not found \t[\033[1;31mFail\033[0m]\n"
    sys.exit(5)

#check file against shooters "no file" message
#print "Checking against "+no_sub_file
f = open(fileName,'rb')
t = open(no_sub_file,'rb')
import hashlib
h = hashlib.sha1()
i = hashlib.sha1()
h.update(f.read())
hash = h.hexdigest()
i.update(t.read())
hash1 = i.hexdigest()
f.close()
t.close()
#print hash
#print hash1
if (hash == hash1) :
    #print "No subs found"
    os.remove(fileName)
    sys.exit(6)

#check langauge against valid languages
#print "checking for lang"
f = open(fileName,'r+')
raw = f.read()
enc =  chardet.detect(raw)['encoding']
text = raw.decode(enc,'ignore')
lang = guessLanguageTag(text)
noValid = True
if any(lang in s for s in validLang):
  #print s+" valid lang"
  noValid = False
if noValid:
  #print "not valid lang found "+lang
  os.remove(fileName)
  sys.exit(7)

#write out file with specified encoding
if enc not in destCode:
  print enc+" not in desired "+destCode
  out = text.encode(destCode, "ignore")
  f.seek(0)
  f.truncate()
  f.write(out)
f.close()

