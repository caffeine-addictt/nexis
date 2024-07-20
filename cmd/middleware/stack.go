package middleware

import "net/http"

type Middleware func(http.Handler) http.Handler

// To create a stack of middlewares
// more cleanly
func CreateStack(stack ...Middleware) Middleware {
	return func(next http.Handler) http.Handler {
		for i := len(stack) - 1; i >= 0; i-- {
			next = stack[i](next)
		}
		return next
	}
}
