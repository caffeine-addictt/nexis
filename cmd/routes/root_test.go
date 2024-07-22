package routes_test

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/caffeine-addictt/nexis/cmd/routes"
)

func TestRootHandler(t *testing.T) {
	t.Run("Root page can be accessed", func(t *testing.T) {
		request := httptest.NewRequest(http.MethodGet, "/", http.NoBody)
		responseRecorder := httptest.NewRecorder()

		routes.GetRoot(responseRecorder, request)

		if responseRecorder.Code != http.StatusOK {
			t.Errorf("Want status code %d, got %d", http.StatusOK, responseRecorder.Code)
		}

		body := responseRecorder.Body.String()

		if !strings.Contains(body, "https://github.com/caffeine-addictt/nexis") {
			t.Errorf("Want body to contain 'https://github.com/caffeine-addictt/nexis', got %s", body)
		}

		if !strings.Contains(body, "Alex Ng <contact@ngjx.org>") {
			t.Errorf("Want body to contain 'Alex Ng <contact@ngjx.org>', got %s", body)
		}
	})
}
