#!/bin/sh

echo 'Starting'
sleep 20
python3 /home/pi/Documents/HouseGuardServices/Build-LED/main.py /home/pi/Documents/run.log 2&>1
