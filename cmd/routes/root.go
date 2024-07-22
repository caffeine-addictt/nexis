package routes

import (
	"fmt"
	"net/http"
)

const RootPageHTML = `
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>NYP InfoSec Auth Service</title>
	</head>
	<body style="background-color: #373737;margin: 0;display: flex;flex-direction: column;align-items: center;justify-content: center;text-color: #fff;min-height: 100vh;max-height: 100vh;min-width: 100vw;max-width: 100vw">
		<h1>Nexis - NYP InfoSec Auth Service</h1>
		<p>Source available on <a href="https://github.com/caffeine-addictt/nexis">GitHub</a>.</p>
		<p>Copyright &copy; 2024 <a href="https://ngjx.org">Alex Ng <contact@ngjx.org></a>. All rights reserved.</p>
	</body>
</html>
`

func GetRoot(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	w.WriteHeader(http.StatusOK)
	fmt.Fprint(w, RootPageHTML)
}
