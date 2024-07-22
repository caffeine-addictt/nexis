package cmd

import (
	"fmt"
	"log"

	"github.com/caffeine-addictt/nexis/cmd/utils"
	"github.com/joho/godotenv"
)

func init() {
	if err := godotenv.Load(); err != nil {
		log.Printf("error loading .env file: %s, continueing with defaults...", err)
	}

	if err := utils.LoadEnvironment(); err != nil {
		panic(err)
	}
}

func Execute() {
	server := NewAPIServer(fmt.Sprintf(":%d", utils.Environment.Port))
	log.Fatalf("Server crashed: %s", server.Run())
}
