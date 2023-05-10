package main

import (
	//"fmt"
	"net/http"
	//"net/url"
)

func main() {
	http.HandleFunc("/", HelloServer)
	http.ListenAndServe(":8080", nil)
}

func HelloServer(w http.ResponseWriter, r *http.Request) {
	//m, _ := url.ParseQuery(r.URL.RawQuery)
	//fmt.Fprintf(w, "Hello, %s!", m["q"])
    http.Redirect(w, r, "https://deepfloyd-if.hf.space/", http.StatusSeeOther)
}
