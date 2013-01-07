shooterSub
==========

Automated solution to grab chinese subtitles from http://www.shooter.cn

#dependancies
- dev-python/guess-language
- dev-python/chardet

#install
- copy shooterSub.ini and nosubs.srt to /etc/shootersub
- copy getSub.py and shooterSub.py to /usr/bin

#configure
- edit shooterSub.ini to point to your video library 

#automate
- add getSub.py to your crontab
    
	$ 0 8 * * * sudo /usr/bin/getSub.py > /var/log/getSub.log
