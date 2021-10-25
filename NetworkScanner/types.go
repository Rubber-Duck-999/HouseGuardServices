package main

type ConfigTypes struct {
	Devices []Device `yaml:"devices"`
}

type Device struct {
	Name    string `yaml:"name"`
	Mac     string `yaml:"mac"`
	Ip      string `json:"ip"`
	Alive   bool   `json:"alive"`
	Allowed int    `json:"allowed"`
}

type Scan struct {
	Devices []Device
	File    string
}

const ALLOWED int = 1
const BLOCKED int = 2
const UNKNOWN int = 3
