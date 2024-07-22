package v1

import (
	"encoding/json"
	"net/http"

	"github.com/caffeine-addictt/nexis/cmd/types"
)

func GetOk(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	resp := &types.APISuccessResponse[string]{
		Status: http.StatusOK,
	}
	json.NewEncoder(w).Encode(resp)
}
