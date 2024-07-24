package v1_test

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	v1 "github.com/caffeine-addictt/nexis/cmd/routes/api/v1"
	"github.com/caffeine-addictt/nexis/cmd/types"
	"github.com/caffeine-addictt/nexis/cmd/utils"
)

func TestUpHandler(t *testing.T) {
	t.Run("/api/v1/up always is up", func(t *testing.T) {
		request := httptest.NewRequest(http.MethodGet, "/", http.NoBody)
		responseRecorder := httptest.NewRecorder()

		v1.GetUp(responseRecorder, request)

		// Check response code
		if responseRecorder.Code != http.StatusOK {
			t.Errorf("Want status code %d, got %d", http.StatusOK, responseRecorder.Code)
		}

		// Check header
		contentType := responseRecorder.Header().Get("Content-Type")
		if contentType != "application/json" {
			t.Errorf("Want content type %s, got %s", "application/json", contentType)
		}

		body := responseRecorder.Body.String()
		expected := strings.Builder{}

		// Write struct to JSON string
		err := utils.TryWriteJson(&expected, &types.APISuccessResponse[string]{
			Status: http.StatusOK,
			Data:   "Up!",
		})
		if err != nil {
			t.Errorf("Failed to encode and write expected JSON response: %v", err)
		}

		// Check payload
		if body != expected.String() {
			t.Errorf("Want body %s, got %s", expected.String(), body)
		}
	})
}
