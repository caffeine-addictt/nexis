package cmd

import (
	"log"
	"net/http"
	"time"

	"github.com/caffeine-addictt/nexis/cmd/middleware"
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
		middleware.RateLimiterMiddleware,
		middleware.RequestLogger,
	)

	server := http.Server{
		Addr:           s.addr,
		Handler:        stack(router),
		ReadTimeout:    10 * time.Second,
		WriteTimeout:   10 * time.Second,
		IdleTimeout:    120 * time.Second,
		MaxHeaderBytes: 1 << 20, // 1 MB
	}

	log.Println("Starting server on", s.addr)
	return server.ListenAndServe()
}
