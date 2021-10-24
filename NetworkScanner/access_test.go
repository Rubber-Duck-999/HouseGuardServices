// access_test.go (access-check)

package main

import (
	"testing"
)

// We can check the file exist
// then run this test will prove it checks correctly exists
func TestExistFile(t *testing.T) {
	var this_file string = `config.yml-sample`
	if Exists(this_file) == true {
		t.Error("Failure TestExistFile")
	}
}

// We can check the file doesn't exist
// then run this test will prove it checks correctly
func TestDoesntExistFile(t *testing.T) {
	var this_file string = `cheese.txt`
	if Exists(this_file) == true {
		t.Error("Failure DoesntExistFile")
	}
}

// We can check the folder exists
// then run this test will prove it checks correctly exists
func TestFolderInvalid(t *testing.T) {
	var this_file string = `pkg`
	if Exists(this_file) == true {
		t.Error("Failure FolderInvalid")
	}
}

func TestConfigGetNull(t *testing.T) {
	var file string = `config.yml-sample`
	var data ConfigTypes
	GetData(&data, file)
	if data.Settings.Code != "" {
		t.Error("Failure")
	}
	if data.Settings.Url != "" {
		t.Error("Failure")
	}
}

func TestConfigGetAll(t *testing.T) {
	var file string = `../config.yml-sample`
	var data ConfigTypes
	if GetData(&data, file) == false {
		t.Error("Failure")
	}
	if data.Settings.Code == "" {
		t.Error("Failure")
	}
}

func TestConfigFail(t *testing.T) {
	var file string = `config.ymlsample`
	var data ConfigTypes
	if GetData(&data, file) == true {
		t.Error("Failure")
	}
	if data.Settings.Code != "" {
		t.Error("Failure")
	}
	if data.Settings.Url != "" {
		t.Error("Failure")
	}
}

func TestIncorrectConfig(t *testing.T) {
	var file string = `config.yml-fail`
	var data ConfigTypes
	if GetData(&data, file) == true {
		t.Error("Failure")
	}
	if data.Settings.Code != "" {
		t.Error("Failure")
	}
	if data.Settings.Url != "" {
		t.Error("Failure")
	}
}
