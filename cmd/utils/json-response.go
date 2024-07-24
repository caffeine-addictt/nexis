package utils

import (
	"encoding/json"
	"errors"
	"io"
	"log"
	"net/http"

	"github.com/caffeine-addictt/nexis/cmd/types"
)

// Try to marshal data and write it to io.Writer
func TryWriteJson(w io.Writer, data any) error {
	marshal, err := json.Marshal(data)
	if err != nil {
		return err
	}

	if _, err := w.Write(marshal); err != nil {
		return err
	}

	return nil
}

// Try to marshal data and write it to http response.
// Writes a 500 error if it fails to marshal.
func TryWriteJsonResponse(w http.ResponseWriter, code int, data any) error {
	marshal, err := json.Marshal(data)
	if err != nil {
		// Write 500 status
		marshal, internalErr := json.Marshal(&types.APIErrorResponse{
			Status:  http.StatusInternalServerError,
			Message: http.StatusText(http.StatusInternalServerError),
		})
		if internalErr != nil {
			return errors.Join(err, internalErr)
		}

		w.WriteHeader(http.StatusInternalServerError)
		if _, internalErr = w.Write(marshal); internalErr != nil {
			return errors.Join(err, internalErr)
		}

		return err
	}

	w.WriteHeader(code)
	if _, err := w.Write(marshal); err != nil {
		return err
	}

	return nil
}

// Invokes TryWriteJsonResponse.
// StdOut and returns a false on error
func WriteJsonResponse(w http.ResponseWriter, code int, data any) bool {
	if err := TryWriteJsonResponse(w, code, data); err != nil {
		log.Println("Failed to encode and write JSON response:", err)
		return false
	}
	return true
}
