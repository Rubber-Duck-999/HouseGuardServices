package main

import (
	"os"

	"github.com/akamensky/argparse"
	log "github.com/sirupsen/logrus"
)

func main() {
	log.SetLevel(log.DebugLevel)
	customFormatter := new(log.TextFormatter)
	customFormatter.TimestampFormat = "2006-01-02 15:04:05"
	log.SetFormatter(customFormatter)
	customFormatter.FullTimestamp = true
	log.Warn("NAC - Beginning to run Network ScannerProgram")
	parser := argparse.NewParser("file", "Config file for runtime purpose")
	// Create string flag
	f := parser.String("f", "config", &argparse.Options{Required: true, Help: "Necessary config"})
	// Parse input
	err := parser.Parse(os.Args)
	if err != nil {
		// In case of error print error and print usage
		// This can also be done by passing -h or --help flags
		log.Error(parser.Usage(err))
		os.Exit(2)
	}

	file := *f
	var data ConfigTypes
	if Exists(file) {
		GetData(&data, file)
		found := make([]Device, 0)
		scan := Scan{
			Devices: data.Devices,
			Found:   found,
		}
		scan.checkDevices()
	} else {
		log.Error("File doesn't exist")
		os.Exit(2)
	}
}
