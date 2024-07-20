package cmd

import (
	"log"
	"os"
	"strconv"

	"github.com/joho/godotenv"
)

type Config struct {
	Env   string
	Port  int
	Debug bool
}

var Environment = &Config{}

func loadEnvironment() {
	// Parse ENV
	Environment.Env = "development"
	if env, set := os.LookupEnv("ENV"); set {
		Environment.Env = env
	}

	// Only care about .env file if not in production
	if Environment.Env != "production" {
		if err := godotenv.Load(); err != nil {
			log.Fatalf("Error loading .env file: %s", err)
		}
	}

	// Parse DEBUG
	Environment.Debug = false
	if debug, set := os.LookupEnv("DEBUG"); set {
		Environment.Debug = debug == "true"
	}

	// Parse PORT
	Environment.Port = 3000
	if port, set := os.LookupEnv("PORT"); set {
		parsedPort, err := strconv.Atoi(port)
		if err != nil {
			log.Fatalf("Error parsing PORT: %s", err)
		}

		Environment.Port = parsedPort
	}
}
