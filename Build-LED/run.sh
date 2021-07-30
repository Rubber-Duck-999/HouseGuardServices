#!/bin/sh

echo 'Starting'
sleep 20
python3 /home/pi/Documents/HouseGuardServices/Build-LED/main.py 2&>1 /home/pi/Documents/run.log
