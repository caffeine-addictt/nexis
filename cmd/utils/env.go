package utils

import (
	"fmt"
	"os"
	"strconv"

	"github.com/joho/godotenv"
)

type Config struct {
	// Env is the environment to run the server in.
	// Either "production" or "development".
	// Optional, ENV: Defaults to "development"
	Env string

	// The secret key used to sign and verify JWT access tokens.
	// Please ensure this is at least 32 characters long, random and not guessable.
	// Required, JWT_ACCESS_SECRET
	JwtAccessSecret string

	// The secret key used to sign and verify JWT refresh tokens.
	// Please ensure this is at least 32 characters long, random and not guessable.
	// Required, JWT_REFRESH_SECRET
	JwtRefreshSecret string

	// The port for the server to listen on.
	// Optional, PORT: Defaults to 3000
	Port int
}

var Environment = &Config{}

func LoadEnvironment() error {
	// Only care about .env file if not in production
	if Environment.Env != "production" {
		if err := godotenv.Load(); err != nil {
			return fmt.Errorf("error loading .env file: %s", err)
		}
	}

	// Parse ENV Environment.Env = "development"
	if env, set := os.LookupEnv("ENV"); set {
		Environment.Env = env
	}
	if Environment.Env != "development" && Environment.Env != "production" {
		return fmt.Errorf("ENV must be either 'development' or 'production'")
	}

	// Parse PORT
	Environment.Port = 3000
	if port, set := os.LookupEnv("PORT"); set {
		parsedPort, err := strconv.Atoi(port)
		if err != nil {
			return fmt.Errorf("error parsing PORT: %s", err)
		}

		Environment.Port = parsedPort
	}

	// Parse JWT_ACCESS_SECRET
	if jwtAccessSecret, set := os.LookupEnv("JWT_ACCESS_SECRET"); set {
		// Ensure JWT_SECRET is long, random and not guessable
		if len(jwtAccessSecret) < 64 {
			return fmt.Errorf("JWT_SECRET must be at least 32 characters long")
		}
		Environment.JwtAccessSecret = jwtAccessSecret
	} else {
		return fmt.Errorf("JWT_ACCESS_SECRET must be set")
	}

	// Parse JWT_REFRESH_SECRET
	if jwtRefreshSecret, set := os.LookupEnv("JWT_REFRESH_SECRET"); set {
		// Ensure JWT_SECRET is long, random and not guessable
		if len(jwtRefreshSecret) < 64 {
			return fmt.Errorf("JWT_SECRET must be at least 32 characters long")
		}
		Environment.JwtRefreshSecret = jwtRefreshSecret
	} else {
		return fmt.Errorf("JWT_REFRESH_SECRET must be set")
	}

	return nil
}
