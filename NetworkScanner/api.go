package main

import (
	"encoding/json"
	"io/ioutil"
	"net/http"

	log "github.com/sirupsen/logrus"
)

func getDevices() (err error) {
	log.Debug("Starting the application")
	err = nil
	response, err := http.Get("http://192.168.0.15:5000/devices")
	if err != nil {
		log.Error("The HTTP request failed with error: ", err)
		return err
	} else {
		data, _ := ioutil.ReadAll(response.Body)
		var message Scan
		json.Unmarshal(data, &message)
		for _, device := range message.Devices {
			log.Debug(device)
		}
	}
	return err
}
