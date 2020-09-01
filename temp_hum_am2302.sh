#!/bin/sh

SRCD="/home/pi/SensorScripts/"
TGTD="/home/pi/SensorScripts/Log/"
LOGFILE=$TGTD$(date +%Y%m%d).log
 
/usr/bin/python3 $SRCD/am2302.py >> $LOGFILE
