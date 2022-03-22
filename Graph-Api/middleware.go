package main

import (
    "fmt"
    "net/http"
)


func homePage(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Welcome to the HomePage!")
    fmt.Println("Endpoint Hit: homePage")
}

func returnTemperature(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Temperature")
}


func createNewTemperature(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Received")
}