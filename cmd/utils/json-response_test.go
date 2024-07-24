package utils_test

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/caffeine-addictt/nexis/cmd/types"
	"github.com/caffeine-addictt/nexis/cmd/utils"
)

func TestWriteJsonResponse(t *testing.T) {
	tt := []struct {
		data any
		name string
		code int
		err  bool
	}{
		{
			data: map[string]string{"Test": "Test"},
			name: "should write json response",
			code: 200,
			err:  false,
		},
		{
			data: func() {},
			name: "should not write json response",
			code: 500,
			err:  true,
		},
	}

	for _, tc := range tt {
		t.Run(tc.name, func(t *testing.T) {
			writer := httptest.NewRecorder()

			// Write to response
			err := utils.TryWriteJsonResponse(writer, tc.code, tc.data)
			if (!tc.err && err != nil) || (tc.err && err == nil) {
				t.Errorf("Expected error, got %t", err)
			}

			// Check code
			if writer.Code != tc.code {
				t.Errorf("Expected status code %d, got %d", tc.code, writer.Code)
			}

			// Build expected JSON
			expected := strings.Builder{}
			if tc.err {
				if err := utils.TryWriteJson(&expected, &types.APIErrorResponse{
					Status:  http.StatusInternalServerError,
					Message: http.StatusText(http.StatusInternalServerError),
				}); err != nil {
					t.Errorf("Failed marshal expected JSON: %s", err)
				}
			} else {
				if err := utils.TryWriteJson(&expected, tc.data); err != nil {
					t.Errorf("Failed marshal expected JSON: %s", err)
				}
			}

			// Check JSON
			if writer.Body.String() != expected.String() {
				t.Errorf(`Expected json string "%s", got "%s"`, expected.String(), writer.Body.String())
			}
		})
	}
}
