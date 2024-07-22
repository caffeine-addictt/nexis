package cmd

import (
	"net/http"

	rootHandlers "github.com/caffeine-addictt/nexis/cmd/routes"
	apiV1Handlers "github.com/caffeine-addictt/nexis/cmd/routes/api/v1"
)

// Here is where we will register every single endpoint
func RegisterRoutes(router *http.ServeMux) {
	// Register /
	router.HandleFunc("/", rootHandlers.GetRoot)

	// Register /api/v1
	v1 := http.NewServeMux()
	v1.HandleFunc("GET /up", apiV1Handlers.GetOk)

	router.Handle("/api/v1/", http.StripPrefix("/api/v1", v1))
}
