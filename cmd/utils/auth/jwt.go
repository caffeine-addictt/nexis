package auth

import (
	"time"

	"github.com/golang-jwt/jwt/v5"
)

// How long an access token will remain valid (1 hour)
const AccessTokenLifetime = time.Hour

// How long a refresh token will remain valid (30 days)
const RefreshTokenLifetime = time.Hour * 24 * 30

func CreateToken(userID string, lifetime time.Duration, secret string) (string, error) {
	claims := jwt.NewWithClaims(jwt.SigningMethodHS512, jwt.MapClaims{
		"sub": userID,                          // Identifier
		"iss": "nexis",                         // Issuer
		"exp": time.Now().Add(lifetime).Unix(), // Expiry
		"iat": time.Now().Unix(),               // Issued At
	})

	// Generate token
	token, err := claims.SignedString([]byte(secret))
	if err != nil {
		return "", err
	}

	return token, nil
}

func VerifyToken(token, secret string) (*jwt.MapClaims, error) {
	// Parse token
	claims := jwt.MapClaims{}
	_, err := jwt.ParseWithClaims(token, claims, func(token *jwt.Token) (interface{}, error) {
		return []byte(secret), nil
	})
	if err != nil {
		return nil, err
	}

	return &claims, nil
}
