package cmd

import (
	"net/http"

	rootHandlers "github.com/caffeine-addictt/nexis/cmd/routes"
)

// Here is where we will register every single endpoint
func RegisterRoutes(router *http.ServeMux) {
	// Register /
	router.HandleFunc("/", rootHandlers.GetRoot)
}
