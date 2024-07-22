package utils

import (
	"encoding/json"
	"io"
	"log"
)

func WriteJsonResponse(w io.Writer, data any) {
	// Try to write struct into JSON string
	if err := json.NewEncoder(w).Encode(data); err != nil {
		log.Println("Failed to encode and write JSON response:", err)
	}
}
