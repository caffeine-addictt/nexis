package middleware

import (
	"net/http"
	"time"

	"github.com/caffeine-addictt/nexis/cmd/types"
	"github.com/caffeine-addictt/nexis/cmd/utils"
	"github.com/didip/tollbooth"
	"github.com/didip/tollbooth/limiter"
)

func RateLimiterMiddleware(next http.Handler) http.Handler {
	newLim := tollbooth.NewLimiter(5, &limiter.ExpirableOptions{DefaultExpirationTTL: time.Hour})
	newLim.SetOnLimitReached(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusTooManyRequests)
		utils.WriteJsonResponse(w, &types.APIErrorResponse{
			Status:  http.StatusTooManyRequests,
			Message: http.StatusText(http.StatusTooManyRequests),
		})
	})
	newLim.SetMessage("")

	return tollbooth.LimitFuncHandler(newLim, func(w http.ResponseWriter, r *http.Request) {
		next.ServeHTTP(w, r)
	})
}
