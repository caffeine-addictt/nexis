package types

type APISuccessResponse[T any] struct {
	// Data is the data returned by the API
	Data T `json:"data"`

	// Status is the status code of the response
	Status int `json:"status"`
}

type APIErrorResponse struct {
	// Message is the message that describes the error
	Message string `json:"message"`

	// Status is the status code of the response
	Status int `json:"status"`
}
