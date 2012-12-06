shooterSub
==========

Automated solution to grab chinese subtitles from http://www.shooter.cn

#install
- copy shooterSub.ini and nosubs.srt to /etc/shootersub
- copy getSub.py and shooterSub.py to /usr/local/bin

#configure
- edit shooterSub.ini to point to your video library 

#automate
- add getSub.py to your crontab
    
	$ 0 8 * * * sudo /usr/local/bin/getSub.py > /var/log/getSub.log
