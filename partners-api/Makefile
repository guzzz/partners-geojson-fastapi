#!/bin/bash
.PHONY: default
.SILENT:


default:

shell:
	docker-compose stop api_partners
	docker-compose run --rm --service-ports api_partners bash

start:
	docker-compose up -d
	docker-compose up -d mongo-express

start_api:
	make start
	docker-compose stop api_partners
	docker-compose run --rm --service-ports api_partners

stop:
	docker-compose down

build:
	docker-compose build --force-rm --no-cache --pull

clean:
	make stop
	docker network rm partners-network
	docker image rm $$(docker image ls -q -f reference=partners_api)

setup:
	docker network create partners-network
	make build
	make start
	docker-compose up -d mongo-express

logs:
	docker-compose logs -f

logs_api:
	docker-compose logs -f api_partners

test:
	docker-compose up -d
	docker-compose stop api_partners
	docker-compose run --rm api_partners pytest
