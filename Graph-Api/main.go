
// main.go
package main

import (
    "log"
    "net/http"

    "github.com/gorilla/mux"
)

// Article - Our struct for all articles
type Temperature struct {
    Count   string `json:"Count"`
    Records []string `json:"Records"`
    AverageHumidity    string `json:"AverageHumidity"`
    AverageTemperature string `json:"AverageTemperature"`
}

var Events Temperature

func handleRequests() {
    myRouter := mux.NewRouter().StrictSlash(true)
    myRouter.HandleFunc("/", homePage)
    myRouter.HandleFunc("/temp", returnTemperature)
    myRouter.HandleFunc("/temp", createNewTemperature).Methods("POST")
    log.Fatal(http.ListenAndServe(":10000", myRouter))
}

func main() {
    Events = Temperature{
        Count: "0",
        Records: []string,
        AverageHumidity: "22",
        AverageTemperature: "22",
    }
    handleRequests()
}