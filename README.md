# HouseGuardServices

Services for the houseguard system in one place

## Serrvices

* Alarm GUI
    * GUI for displaying alarm status and switchign on and off
* Emailer
    * Notifier for the whole project
* Motion
    * Notifies of motion on sensor
* Status GUI
    * Displays data on weather, motion and others
* Weather
    * Sensor for temperature

## Start-up

`sudo nano /home/pi/.config/lxsession/LXDE-pi/autostart`

Inside the file place the python script you want to run

`/home/pi/Documents/HouseGuardServices/Status-GUI/main.py`

## READMEs

* [Alarm-GUI](./Alarm-GUI/README.md)
* [Emailer](./Emailer/README.md)
* [Motion](./Motion/README.md)
* [Status-GUI](./Status-GUI/README.md)
* [Weather](./Weather/README.md)