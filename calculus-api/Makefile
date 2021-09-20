#!/bin/bash
.PHONY: default
.SILENT:


default:

shell:
	docker-compose stop api_calculus
	docker-compose run --rm --service-ports api_calculus bash

start:
	docker-compose up -d
	docker-compose up -d mongo-express-calculus

start_api:
	docker-compose up -d
	docker-compose stop api_calculus
	docker-compose run --rm --service-ports api_calculus

stop:
	docker-compose down

build:
	docker-compose build --force-rm --no-cache --pull

clean:
	make stop
	docker network rm calculus-network
	docker image rm $$(docker image ls -q -f reference=calculus_api)

setup:
	docker network create calculus-network
	make build
	make start
	docker-compose up -d mongo-express-calculus

logs:
	docker-compose logs -f

logs_api:
	docker-compose logs -f api_calculus

test:
	docker-compose up -d
	docker-compose stop api_calculus
	docker-compose run --rm api_calculus pytest
