package v1

import (
	"net/http"

	"github.com/caffeine-addictt/nexis/cmd/types"
	"github.com/caffeine-addictt/nexis/cmd/utils"
)

func GetUp(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	utils.WriteJsonResponse(w, http.StatusOK, &types.APISuccessResponse[string]{
		Status: http.StatusOK,
		Data:   "Up!",
	})
}
