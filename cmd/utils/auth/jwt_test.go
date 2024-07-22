package auth_test

import (
	"testing"
	"time"

	"github.com/caffeine-addictt/nexis/cmd/utils/auth"
)

func TestJwtFunctionality(t *testing.T) {
	userIDPool := []string{"a", "user", "45c5f3bb-95fb-4688-b50d-15f7d987e752", "c487251e-f502-4140-9198-608ca615efe4"}
	secretsPool := []string{"secret", "mysecret", "verysecretsecret"}

	for _, userID := range userIDPool {
		t.Run("Generated JWT can be validated", func(t *testing.T) {
			for _, secret := range secretsPool {
				// Create token
				token, err := auth.CreateToken(userID, time.Hour, secret)
				if err != nil {
					t.Errorf("Generating a JWT token failed\nUserID:%s\nSecret:%s\nError:%s", userID, secret, err)
				}

				// Make sure token is not empty
				if token == "" {
					t.Errorf("Generating a JWT token gave an empty string\nUserID:%s\nSecret:%s", userID, secret)
				}

				// Verify token
				claims, err := auth.VerifyToken(token, secret)
				if err != nil {
					t.Errorf("Decoding a JWT token failed\nUserID:%s\nSecret:%s\nError:%s", userID, secret, err)
				}

				// Parse sub
				sub, err := claims.GetSubject()
				if err != nil {
					t.Errorf("Failed to get sub from claims\nUserID:%s\nSecret:%s\nError:%s", userID, secret, err)
				}

				// Ensure sub is userID
				if sub != userID {
					t.Errorf("Decoding a JWT token gave wrong sub\nUserID:%s\nSecret:%s\nGot:%s", userID, secret, sub)
				}
			}
		})
	}
}
