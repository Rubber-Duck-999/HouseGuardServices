package main

import (
	log "github.com/sirupsen/logrus"
)

func main() {
	log.SetLevel(log.DebugLevel)
	customFormatter := new(log.TextFormatter)
	customFormatter.TimestampFormat = "2006-01-02 15:04:05"
	log.SetFormatter(customFormatter)
	customFormatter.FullTimestamp = true
	log.Warn("NAC - Beginning to run Network Scanner Program")
	a := make([]Device, 0)
	scan := Scan{
		Devices: a,
		Count:   0,
	}
	err := scan.getDevices()
	if err != nil {
		log.Error("Error found on api GET")
	} else {
		scan.checkDevices()
	}
}
