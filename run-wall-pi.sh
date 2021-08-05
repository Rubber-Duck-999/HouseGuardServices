#!/bin/sh

echo 'Starting'
python3 /home/pi/Documents/HouseGuardServices/Motion/main.py &

python3 /home/pi/Documents/HouseGuardServices/Alarm-GUI/main.py &
