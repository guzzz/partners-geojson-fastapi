#!/bin/bash
.PHONY: default
.SILENT:


default:

start:
	make startcalculus
	make startpartners

startcalculus:
	cd calculus-api; \
	make start

startpartners:
	cd partners-api; \
	make start

stop:
	make stopcalculus
	make stoppartners

stopcalculus:	
	cd calculus-api; \
	make stop

stoppartners:
	cd partners-api; \
	make stop

setup:
	make setupcalculus
	make setuppartners

setupcalculus:
	cp .env-example calculus-api/.env
	cd calculus-api; \
	make setup

setuppartners:
	cp .env-example partners-api/.env
	cd partners-api; \
	make setup

test:
	make testcalculus
	make testpartners

testcalculus:
	make startcalculus
	cd calculus-api; \
	docker-compose stop api_calculus; \
	docker-compose run --rm api_calculus pytest; \
	docker-compose stop api_calculus; \
	docker-compose up -d api_calculus; \

testpartners:
	make startpartners
	cd partners-api; \
	docker-compose stop api_partners; \
	docker-compose run --rm api_partners pytest; \
	docker-compose stop api_partners; \
	docker-compose up -d api_partners; \

clear:
	make stop
	docker network rm partners-network calculus-network
	docker volume rm mongodb-data calculus-mongodb-data
