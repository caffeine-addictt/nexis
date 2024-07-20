package cmd

import (
	"log"
	"net/http"

	"github.com/caffeine-addictt/auth-nyp-infosec/cmd/middleware"
)

type APIServer struct {
	addr string
}

func NewAPIServer(addr string) *APIServer {
	return &APIServer{
		addr: addr,
	}
}

func (s *APIServer) Run() error {
	router := http.NewServeMux()
	RegisterRoutes(router)

	stack := middleware.CreateStack(
		middleware.RequestLogger,
	)

	server := http.Server{
		Addr:    s.addr,
		Handler: stack(router),
	}

	log.Println("Starting server on", s.addr)
	return server.ListenAndServe()
}
