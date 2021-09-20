<p align="center">

![alt text](https://i.imgur.com/2UcpZsA.png)

</p>

<p align="center">
<img src="https://img.shields.io/badge/docker-20.10.08-blue"/>
<img src="https://img.shields.io/badge/docker--compose-1.29.2-9cf"/>
<img src="https://img.shields.io/badge/python-3.8-yellowgreen"/>
<img src="https://img.shields.io/badge/framework-fastAPI-brightgreen"/>
<img src="https://img.shields.io/badge/mongo-5.0.2--focal-green"/>
<img src="https://img.shields.io/badge/redis-6.2.5--alpine-red"/>
</p>

---

<h1 align="center">
   🚀 Partners GeoJSON FastAPI
</h1>
<p align="center">
    <em>
    Decentralized system for registration and management of partners and calculus about proximity
    </em>
</p>

---

Summary
=================

   * [The project](#the-project)
   * [Specifications](#specifications)
   * [Swagger (OpenAPI)](#swagger-openapi)
   * [Endpoints](#endpoints-partners-api)
      * [partners-api](#endpoints-partners-api)
      * [calculus-api](#endpoints-calculus-api)
   * [Makefile](#makefile)
   * [Run Locally](#run-locally)
   * [Tests](#tests)
   * [Requirements](#requirements)

---

## The project

The main features of the system are:

1. Partners creation. The data inputs of each user are: id, tradingName, ownerName, document, coverageArea and address.
2. The address field follows the GeoJSON Point format.
3. The coverageArea field follows the GeoJSON MultiPolygon format.
4. The id and document fields are unique fields.
5. Partners list and retrieves.
6. Given a specific location (coordinates lat and long), search the nearest partner which the coverage area includes the location.

Obs.: In addition to these, some other features were included, such as: cache layers, paging listing and configurable page size.

---

## Specifications

This project uses event driven architecture (EDA).

The system consists of:

1. API Python FastAPI + MongoDB.
2. API Python FastAPI + MongoDB.
3. Redis layers for both APIs.
4. Broker RabbitMQ.
5. Docker + Docker-compose.

Organization:

1. partners-api:

API responsible for managing partners. Partner-related activities generate events that seek to keep partner data in the calculus-api consistent. This API uses a lot of validation on partner infos. The indexes created are related to retrieve activities only.

2. calculus-api:

API responsible for proximity calculus. This API also uses Mongodb, however, the indexes created are 2dsphere indexes. This indexes are related to the research of nearest partners.

---

## Swagger (OpenAPI)

Both APIs uses fastAPI, so they are documented with OpenAPI. The projects documentation can be found in the "/docs" and "/redoc" endpoints.

* partners-api: http://localhost:8000/docs
* calculus-api: http://localhost:8001/docs

---

## Endpoints partners-api

1. **(GET)** **_"/v0/partners/"_** - *Returns all partners registered.*
2. **(POST)** **_"/v0/partners/"_** - *Register a new partner.*
3. **(GET)** **_"/v0/partners/{id}"_** - *Returns a specific partner.*


#### Specifications

1. The endpoint for listing partners have 2 additional parameters that can be sent in the headers in order to paginate the results:

* page ( page number )
* limit ( page size )

2. The creation endpoint accepts integer ID or string ID. However, it's not mandatory to send an ID. In that case, the system will generate a new UUID to the partner.

_Obs._: It runs in: http://localhost:8000/

---

## Endpoints calculus-api

1. **(POST)** **_"/v0/nearest/"_** - *Returns the nearest partner which the coverage area includes the location sent.*


#### Specifications

My choice for a *POST* endpoint instead of other options was related to some observations:

1. Despite this endpoint is classified as a "safe" endpoint, it's not "idempotent". Everytime a new partner is added in the system, this endpoint's return may change.
2. Sending the request as a body POST, I could treat it as a form. So, this strategy made it possible to implement easy and fast validation, with the frameworks help.

_Obs._: It runs in: http://localhost:8001/

---

## Makefile

Both APIs have a _Makefile_ in their root. However, in this project root there is this third _Makefile_ to facilitate the entire system usage. The main commands are:

* **_make setup_**: Setup the entire environment to run the projects. Only need to use this command once.
* **_make stop_**: Stop all containers.
* **_make start_**: Create containers and run the API's.
* **_make test_**: Run all tests.
* **_make clear_**: Clean this project's containers, images, volumes and network from your computer. It's recommended to read this Makefile command before you use it, to make sure that you do not have other projects with similar names.

---

## Run Locally

1. Make sure you have the Docker and Docker-compose installed.
2. Go into the **.env-example** and review the environment vars: The redis expiration time is important to understand the system, and the AMQP URL was already setted by me to evaluation purposes.
3. In the first time running the project (and just in the first one) you will have to use the command **make setup** .
3. Next time, you will just have to use **make start** and **make stop** commands.

* Each API have their own Makefile archive, in case you want to run each project individually.
* The command **make logs_api** and **make logs** helps to visualize the system logs.

---

## Tests

==> There are 13 tests being tested in this project. The characteristics of this tests can be readden below:

1. [partners-api] Seven tests running in the partners app.
2. [calculus-api] Six tests running in the calculus app.

* To test the system, just run the command **make test** ( remembering that if it is the first time to run the project, the command "make setup" must run first )

---

## Requirements

* **DOCKER-COMPOSE**: 1.29.2
* **DOCKER**: 20.10.08
