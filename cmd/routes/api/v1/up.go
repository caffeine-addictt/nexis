package v1

import (
	"net/http"

	"github.com/caffeine-addictt/nexis/cmd/types"
	"github.com/caffeine-addictt/nexis/cmd/utils"
)

func GetOk(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	utils.WriteJsonResponse(w, &types.APISuccessResponse[string]{
		Status: http.StatusOK,
		Data:   "Up!",
	})
}
