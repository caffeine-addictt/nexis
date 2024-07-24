package middleware

import (
	"context"
	"net/http"
	"strings"

	"github.com/caffeine-addictt/nexis/cmd/types"
	"github.com/caffeine-addictt/nexis/cmd/utils"
	"github.com/caffeine-addictt/nexis/cmd/utils/auth"
	"github.com/golang-jwt/jwt/v5"
)

type authUserKey string

const AuthUserID = authUserKey("middleware.auth.userID")

// To Handle returning 401
func writeUnauthed(w http.ResponseWriter) {
	utils.WriteJsonResponse(w, http.StatusUnauthorized, &types.APIErrorResponse{
		Status:  http.StatusUnauthorized,
		Message: http.StatusText(http.StatusUnauthorized),
	})
}

// Middleware to pass the user id in the context
// This middleware will NOT return a 401. It will only
// attempt to parse the userId from the Authorization header (if any).
//
// Use EnsureAuthMiddleware after this middleware to raise a 401
func ParseAuthMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		authorization := r.Header.Get("Authorization")

		// Check if Authorization header is set
		if !strings.HasPrefix(authorization, "Bearer ") {
			next.ServeHTTP(w, r)
			return
		}

		// Pull out token
		encodedToken := strings.TrimPrefix(authorization, "Bearer ")

		// Decode token assuming its an access token
		var claims *jwt.MapClaims
		if accessClaims, err := auth.VerifyToken(encodedToken, utils.Environment.JwtAccessSecret); err != nil {
			// Decode token assuming its a refresh token
			refreshClaims, err := auth.VerifyToken(encodedToken, utils.Environment.JwtRefreshSecret)
			if err != nil {
				next.ServeHTTP(w, r)
				return
			}
			claims = refreshClaims
		} else {
			claims = accessClaims
		}

		// Parse userId
		userID, err := claims.GetSubject()
		if err != nil {
			next.ServeHTTP(w, r)
			return
		}

		// Using context to pass userId down
		ctx := context.WithValue(r.Context(), AuthUserID, userID)
		next.ServeHTTP(w, r.WithContext(ctx))
	})
}

// Middleware to ensure that the user is authenticated
// Ensure that "ParseAuthMiddleware" is called before this or
// a 401 will be returned every single time.
func EnsureAuthMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		userID := r.Context().Value(AuthUserID)

		// See if userID was not set
		if userID == nil {
			writeUnauthed(w)
			return
		}

		next.ServeHTTP(w, r)
	})
}
