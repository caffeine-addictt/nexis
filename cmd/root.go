package cmd

import (
	"fmt"
	"log"
)

func init() {
	loadEnvironment()
}

func Execute() {
	server := NewAPIServer(fmt.Sprintf(":%d", Environment.Port))
	log.Fatalf("Server crashed: %s", server.Run())
}
