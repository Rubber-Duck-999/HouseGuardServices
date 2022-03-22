
// main.go
package main

import (
    "log"
    "net/http"

    "github.com/gorilla/mux"
)

func handleRequests() {
    myRouter := mux.NewRouter().StrictSlash(true)
    myRouter.HandleFunc("/", homePage)
    myRouter.HandleFunc("/temp", returnTemperature)
    myRouter.HandleFunc("/temp", createNewTemperature).Methods("POST")
    log.Fatal(http.ListenAndServe(":10000", myRouter))
}

func main() {
    handleRequests()
}