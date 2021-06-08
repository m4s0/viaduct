.DEFAULT_GOAL:=help

.PHONY: init
init: build up

.PHONY: build
build:
	docker-compose build

.PHONY: up
up:
	docker-compose up -d

.PHONY: down
down:
	docker-compose down

.PHONY: down-remove-volume
down-remove-volume:
	docker-compose down -v

.PHONY: bash
bash:
	docker-compose run python bash

.PHONY: tests
tests: functional

.PHONY: functional
functional:
	docker-compose run --rm api sh -c 'pytest tests/functional/ -v'
