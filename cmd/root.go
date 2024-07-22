package cmd

import (
	"fmt"
	"log"

	"github.com/caffeine-addictt/nexis/cmd/utils"
)

func init() {
	utils.LoadEnvironment()
}

func Execute() {
	server := NewAPIServer(fmt.Sprintf(":%d", utils.Environment.Port))
	log.Fatalf("Server crashed: %s", server.Run())
}
