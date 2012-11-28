shooterSub
==========

Automated solution to grab chinese subtitles from http://www.shooter.cn

#configure
edit getSub.py to specify the directory of your media files
ensure the shooterSub.py directory is correct
ensure shooterSub.py can reference the default message from shooter
    $ t = open('/usr/local/bin/nosubs.srt','rb')


#automate
add getSub.py to your crontab
    $ 0 8 * * * sudo /usr/local/bin/getSub.py
