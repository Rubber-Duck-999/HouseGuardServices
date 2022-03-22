# HouseGuardServices

Services for the houseguard system in one place

## Services

* Graph
    * Generates graph for the temperature and speed
* Network Speed
    * Shows LED lights for speed
* Notifier
    * API for service
* Scheduler
    * Clears the database
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