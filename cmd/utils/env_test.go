package utils_test

import (
	"os"
	"testing"

	"github.com/caffeine-addictt/nexis/cmd/utils"
)

func TestEnvParsing(t *testing.T) {
	tt := []struct {
		inputs map[string]string
		name   string
		errors bool
	}{
		{
			map[string]string{"PORT": "a", "ENV": "production"},
			"Errors on invalid PORT",
			true,
		},
		{
			map[string]string{"PORT": "8080", "ENV": "production"},
			"Does not error on valid PORT",
			true,
		},
		{
			map[string]string{"PORT": "8080", "ENV": "production"},
			"Errors on unset JWT_ACCESS_SECRET",
			true,
		},
		{
			map[string]string{"JWT_ACCESS_SECRET": "a", "PORT": "8080", "ENV": "production"},
			"Errors on too short JWT_ACCESS_SECRET",
			true,
		},
		{
			map[string]string{"PORT": "8080", "JWT_ACCESS_SECRET": "381950a2-25f8-4c53-ab21-ec6074d53470", "ENV": "production"},
			"Errors on unset JWT_REFRESH_SECRET",
			true,
		},
		{
			map[string]string{"JWT_REFRESH_SECRET": "asdad", "JWT_ACCESS_SECRET": "381950a2-25f8-4c53-ab21-ec6074d53470", "PORT": "8080", "ENV": "production"},
			"Errors on too short JWT_REFRESH_SECRET",
			true,
		},
		{
			map[string]string{"JWT_REFRESH_SECRET": "381950a2-25f8-4c53-ab21-ec6074d53470", "JWT_ACCESS_SECRET": "381950a2-25f8-4c53-ab21-ec6074d53470", "PORT": "8080", "ENV": "production"},
			"Does not error on valid JWT_REFRESH_SECRET",
			false,
		},
	}

	for _, tc := range tt {
		t.Run(tc.name, func(t *testing.T) {
			// Set inputs
			for k, v := range tc.inputs {
				os.Setenv(k, v)
			}

			err := utils.LoadEnvironment()

			// Unset inputs
			for k := range tc.inputs {
				os.Unsetenv(k)
			}

			// Check error
			switch err {
			case nil:
				if tc.errors {
					t.Errorf("no error, wantErr")
				}
			default:
				if !tc.errors {
					t.Errorf("error = %v, wantNoErr", err)
				}
			}
		})
	}
}
