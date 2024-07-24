BINARY_NAME:=nexis
PYTHON:=python

ifeq ($(OS),Windows_NT)
RM_CMD:=rd /s /q
NULL:=/dev/nul
else
RM_CMD:=rm -rf
NULL:=/dev/null
endif


# =================================== DEFAULT =================================== #

default: all

## Core: default: Runs build and test
.PHONY: default
all: build

# =================================== HELPERS =================================== #

## Misc: help: print this help message
.PHONY: help
help:
	@echo 'Nexis - You can run the CLI with "poetry run nexis" and the server with "make run"!'
	@echo ''
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Commands:'
	@sed -n 's/^## Core: //p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'
	@echo ''
	@echo 'Misc:'
	@sed -n 's/^## Misc: //p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'
	@echo ''
	@echo 'Extra:'
	@sed -n 's/^## Extra: //p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'




## Core: install: Install dependencies
.PHONY: install
install: install/python install/go install/npm

## Extra: install/python: Install python dependencies
.PHONY: install/python
install/python:
	${PYTHON} -m pip install poetry
	${PYTHON} -m poetry install

## Extra: install/npm: Install npm dependencies
.PHONY: install/npm
install/npm:
	npm i

## Extra: install/go: Install go dependencies
.PHONY: install/go
install/go:
	go get ./...




## Misc: links: Shows the project links
.PHONY: links
links:
	@echo 'Nexis links:'
	@echo ' PyPI Package:           https://pypi.org/project/nexis/'
	@echo ' Github Repository:      https://github.com/caffeine-addictt/nexis'
	@echo ' Official Documentation: https://github.com/caffeine-addictt/nexis/blob/main/docs/index.md'




## Misc: issue: Where to create an issue
.PHONY: issue
issue:
	@echo 'Create an issue at:'
	@echo ' https://github.com/caffeine-addictt/nexis/issues/new'




## Misc: docs: Shows simple development documentation
.PHONY: docs
docs:
	@echo 'Nexis development documentation'
	@echo ''
	@echo 'Prerequisites:'
	@echo ' 1. Python 3.9 or later'
	@echo ' 2. Go 1.22.5 or later'
	@echo ' 3. NPM 10.8.1 or later'
	@echo ' 4. Node 22.3.0 or later'
	@echo ''
	@echo 'Please run the following commands to get started:'
	@echo ' 1. Create a virtual environment with "python -m venv venv"'
	@echo ' 2. Activate the virtual environment with:'
	@echo '     "source venv/bin/activate" on GNU/Linux'
	@echo '     "venv/Scripts/activate.bat" on Windows'
	@echo ' 3. Install the project dependencies with "make install"'
	@echo ''
	@echo 'Steps to run the CLI:'
	@echo ' 1. Install nexis with "poetry install"'
	@echo ' 2. Run the CLI with "poetry run nexis"'
	@echo ''
	@echo 'Steps to run the server:'
	@echo ' 1. Run the server with "make server"'
	@echo ''
	@echo 'Learn more at https://github.com/caffeine-addictt/nexis/blob/main/CONTRIBUTING.md'

# =================================== DEVELOPMENT =================================== #

## Core: build: Builds Python, Go binaries and Docker image
.PHONY: build
build: build/python build/go

## Extra: build/go: Builds the binary
.PHONY: build/go
build/go:
	npx cross-env GOARCH=amd64 GOOS=linux   go build -ldflags="-s -w" -o ./bin/$(BINARY_NAME)-linux main.go
	npx cross-env GOARCH=amd64 GOOS=darwin  go build -ldflags="-s -w" -o ./bin/$(BINARY_NAME)-darwin main.go
	npx cross-env GOARCH=amd64 GOOS=windows go build -ldflags="-s -w" -o ./bin/$(BINARY_NAME)-windows main.go

## Extra: build/python: Builds the binary
.PHONY: build/python
build/python:
	${PYTHON} -m poetry build

## Extra: build/docker: Builds the docker image
.PHONY: build/docker
build/docker:
	@docker > ${NULL} 2> ${NULL} || { echo 'Docker is not installed.'; exit 1; }
	@docker compose > ${NULL} 2> ${NULL} || { echo 'Docker-compose is not installed.'; exit 1; }
	docker compose build




## Core: test: Runs tests
.PHONY: test
test: test/go test/python

## Misc: test/go: Runs Go tests
.PHONY: test/go
test/go:
	go mod verify
	go vet ./...
	go run github.com/securego/gosec/v2/cmd/gosec@latest -quiet ./...
	go run github.com/go-critic/go-critic/cmd/gocritic@latest check -enableAll ./...
	go run github.com/google/osv-scanner/cmd/osv-scanner@latest -r .
	go test -race ./...

## Misc: test/python: Runs Python tests
.PHONY: test/python
test/python:
	${PYTHON} -m poetry run pytest -vv




## Core: server: Run the Go server with docker
.PHONY: server
server:
	@docker > ${NULL} 2> ${NULL} || { echo 'Docker is not installed.'; exit 1; }
	@docker compose > ${NULL} 2> ${NULL} || { echo 'docker compose not found.'; exit 1; }
	docker compose watch

## Misc: server/go-air: Run the Go server with air
.PHONY: server/go-air
server/go-air:
	go run github.com/air-verse/air@latest

# =================================== QUALITY ================================== #

## Core: lint: Lint code
.PHONY: lint
lint: lint/go lint/python lint/npm

## Extra: lint/go: Lint Go code
.PHONY: lint/go
lint/go:
	go run github.com/golangci/golangci-lint/cmd/golangci-lint@latest run

## Extra: lint/python: Lint Python code
.PHONY: lint/python
lint/python:
	${PYTHON} -m poetry run ruff format --check

## Extra: lint/npm: Lint NPM code
.PHONY: lint/npm
lint/npm:
	npm run lint




## Core: format: Format code
.PHONY: format
format: format/go format/python format/npm

## Extra: format/go: Format Go code
.PHONY: format/go
format/go:
	go fmt ./...
	go mod tidy -v
	go run github.com/golangci/golangci-lint/cmd/golangci-lint@latest run --fix

## Extra: format/python: Format Python code
.PHONY: format/python
format/python:
	${PYTHON} -m poetry run ruff format

## Extra: format/npm: Format NPM code
.PHONY: format/npm
format/npm:
	npm run lint:fix




## Core: tidy: Clean up code artifacts
.PHONY: tidy
tidy: tidy/go tidy/python tidy/docker

## Extra: tidy/go: Clean up Go code artifacts
.PHONY: tidy/go
tidy/go:
	go clean ./...
	${RM_CMD} bin
	${RM_CMD} tmp

## Extra: tidy/python: Clean up Python code artifacts
.PHONY: tidy/python
tidy/python:
	${RM_CMD} dist
	${RM_CMD} .pytest_cache
	${RM_CMD} .ruff_cache
	${PYTHON} -Bc "for p in __import__('pathlib').Path('.').rglob('*.py[co]'): p.unlink()"
	${PYTHON} -Bc "for p in __import__('pathlib').Path('.').rglob('__pycache__'): p.rmdir()"

## Extra: tidy/docker: Clean up Docker artifacts
.PHONY: tidy/docker
tidy/docker:
	@docker > ${NULL} 2> ${NULL} || { echo 'Docker is not installed.'; exit 1; }
	@docker compose > ${NULL} 2> ${NULL} || { echo 'docker compose not found.'; exit 1; }

	docker compose down --remove-orphans --rmi local
	@echo 'Docker build cache at $HOME/.cache/go-build/ is not deleted by default.'




## Core: clean: Clean up all artifacts (including venv and node_modules)
.PHONY: clean
clean: tidy/go tidy/python

## Extra: clean/python: Clean up Python venv
.PHONY: clean/python
clean/python:
	${RM_CMD} venv

## Extra: clean/npm: Clean up NPM dependencies
.PHONY: clean/npm
clean/npm:
	${RM_CMD} node_modules
