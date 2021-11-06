package main

import (
	"bytes"
	"encoding/json"
	"io/ioutil"
	"net/http"

	log "github.com/sirupsen/logrus"
)

const url = "http://192.168.0.21:5000/devices"

func (scan *Scan) getDevices() (err error) {
	log.Debug("Starting the application")
	response, err := http.Get(url)
	if err != nil {
		log.Error("The HTTP request failed with error: ", err)
		return err
	} else {
		log.Debug("Success on request")
		data, _ := ioutil.ReadAll(response.Body)
		var message Scan
		json.Unmarshal(data, &message)
		for _, device := range message.Devices {
			scan.Devices = append(scan.Devices, device)
		}
	}
	return err
}

func (scan *Scan) sendNewDevice(device Device) {
	log.Debug("Sending a new device")
	data, err := json.Marshal(device)
	if err != nil {
		log.Warn("Error encoding json")
	}
	jsonStr := []byte(data)
	response, err := http.Post(url, "application/json", bytes.NewBuffer(jsonStr))
	if err != nil {
		log.Error("The HTTP request failed with error: ", err)
	} else {
		data, _ := ioutil.ReadAll(response.Body)
		var message Scan
		json.Unmarshal(data, &message)
		for _, device := range message.Devices {
			log.Debug(device)
		}
	}
}

func (scan *Scan) updateDevice(name string, alive string) {
	log.Trace("Updating a device: ", name, ", Alive: ", alive)
	// marshal User to json
	json, err := json.Marshal(name)
	if err != nil {
		log.Debug(err)
	}
	// initialize http client
	client := &http.Client{}
	// set the HTTP method, url, and request body
	req, err := http.NewRequest(http.MethodPut, url+"/"+alive, bytes.NewBuffer(json))
	if err != nil {
		log.Debug(err)
	}

	// set the request header Content-Type for json
	req.Header.Set("Content-Type", "application/json; charset=utf-8")
	resp, err := client.Do(req)
	if err != nil {
		log.Error(err)
	} else {
		if resp.StatusCode != 200 {
			log.Error("Status code for response is invalid")
		}
	}
}
