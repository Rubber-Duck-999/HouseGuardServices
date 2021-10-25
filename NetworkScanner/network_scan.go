package main

// Mostly based on https://github.com/golang/net/blob/master/icmp/ping_test.go
// All ye beware, there be dragons below...

import (
	"context"
	"io/ioutil"
	"net/http"
	"os/exec"
	"strings"
	"time"

	"github.com/Ullaakut/nmap"
	log "github.com/sirupsen/logrus"
	"gopkg.in/yaml.v2"
)

const (
	ProtocolICMP = 1
)

// Default to listen on all IPv4 interfaces
var ListenAddr = "0.0.0.0"

func (scan *Scan) runARP() {
	log.Debug("### Running ARP ###")
	data, err := exec.Command("arp", "-a").Output()
	if err != nil {
		log.Error(err)
	}

	for id := range scan.Devices {
		scan.Devices[id].Alive = false
	}

	for _, line := range strings.Split(string(data), "\n") {
		fields := strings.Fields(line)
		if len(fields) < 3 {
			continue
		}

		// strip brackets around IP
		ip := strings.Replace(fields[1], "(", "", -1)
		ip = strings.Replace(ip, ")", "", -1)
		new_device := true
		mac := fields[3]
		for id := range scan.Devices {
			if scan.Devices[id].Ip == ip {
				new_device = false
				log.Trace("Device found in Arp table")
				scan.Devices[id].Alive = true
			}
		}
		if new_device {
			if mac != "<incomplete>" {
				log.Warn("Adding device ip: ", ip)
				response, _ := http.Get("https://api.macvendors.com/" + mac)

				defer response.Body.Close()

				data, _ := ioutil.ReadAll(response.Body)

				if response.StatusCode != 200 {
					log.Error("Error on Name")
					data = []byte("Name not Found")
				} else {
					log.Debug("Vendor Name: ", string(data))
				}

				device := Device{string(data), mac, ip, true, UNKNOWN}
				scan.Devices = append(scan.Devices, device)
				time.Sleep(1 * time.Second)
			}
		}
	}
}

func (scan *Scan) nmap_scan() {
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Minute)
	defer cancel()

	// Equivalent to `/usr/local/bin/nmap -p 80,443,843 google.com facebook.com youtube.com`,
	// with a 2 minute timeout.
	scanner, err := nmap.NewScanner(
		nmap.WithTargets("192.168.0.0-255"),
		nmap.WithPorts("80,443,843"),
		nmap.WithContext(ctx),
	)
	if err != nil {
		log.Error("Unable to create nmap scanner: ", err)
	}

	result, warnings, err := scanner.Run()
	if err != nil {
		log.Error("Unable to run nmap scan: ", err)
	}

	if warnings != nil {
		log.Error("Warnings: ", warnings)
	}

	log.Debug("Nmap done: ", len(result.Hosts), " hosts up scanned in seconds ", result.Stats.Finished.Elapsed)
}

func (scan *Scan) checkDevices() {
	for {
		scan.nmap_scan()
		scan.runARP()
		log.Warn("### Devices ###")
		log.Warn("Number of devices - ", len(scan.Devices))
		log.Debug("### End of ARP ###")
		data, err := yaml.Marshal(&scan)
		if err != nil {
			log.Fatal(err)
		}
		err = ioutil.WriteFile(scan.File, data, 0)
		if err != nil {

			log.Fatal(err)
		}
		time.Sleep(30 * time.Second)
	}
}
