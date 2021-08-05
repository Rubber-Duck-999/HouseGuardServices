#!/bin/sh

echo 'Starting'
python3 /home/simon/Documents/HouseGuardServices/Motion/main.py &

python3 /home/simon/Documents/HouseGuardServices/Alarm-GUI/main.py &
