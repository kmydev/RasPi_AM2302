#!/bin/sh

SRCD="/home/pi/SensorScripts/"
TGTD="/home/pi/SensorScripts/Log/"
YMD=$(date +%Y%m%d)
LOGFILE=$TGTD$YMD.log
HTMLFILE=$TGTD$YMD.html
 
/usr/bin/python3 $SRCD/am2302.py >> $LOGFILE

/usr/bin/python3 $SRCD/log2html.py > $HTMLFILE

