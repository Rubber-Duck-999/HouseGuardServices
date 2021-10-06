#!/bin/sh

echo 'Starting'
python3 /home/pi/Documents/HouseGuardServices/Motion/main.py &

python3 /home/pi/Documents/HouseGuardServices/Status-GUI/main.py &

python3 /home/pi/Documents/HouseGuardServices/Notifier/app.py &
