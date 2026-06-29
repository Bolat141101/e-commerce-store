# E-commerce Store API

A small learning REST API for an e-commerce store.

The project uses a simple Python stack:

- `Flask`
- `flask_restful`
- `sqlite3`
- `dataclasses`
- `marshmallow`
- `logging`
- `unittest`
- `Docker`

## Features

- health check endpoint
- Swagger UI documentation
- OpenAPI JSON specification
- simple API client file
- get all goods
- get one good by `id`
- create a good
- update a good
- delete a good
- get all categories
- create a category
- get goods by category
- validate request data with Marshmallow
- log API and database actions

## Project Structure

```text
ecom_store/
├── Dockerfile
├── .dockerignore
├── .gitignore
├── client.py
├── seed_data.py
├── requirements.txt
├── README.md
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── logger_config.py
│   ├── models.py
│   ├── schemas.py
│   ├── swagger.py
│   └── routes.py
└── test/
    ├── README.md
    └── test_routes.py
```

## File Responsibilities

`app/config.py` stores project constants, such as database and table names.

`app/logger_config.py` configures application logging.

`app/models.py` works with the SQLite database.

`app/schemas.py` validates incoming data with `marshmallow`.

`app/routes.py` contains Flask resources, API routes, and app startup code.

`app/swagger.py` contains the OpenAPI specification.

`client.py` is a small client for sending requests to the API.

`seed_data.py` fills the database with default goods for every category.

`test/test_routes.py` contains unit tests for the API.

## Run the Project

Go to the project folder:

```bash
cd my_project/ecom_store
```

Start the server:

```bash
.venv/bin/python app/routes.py
```

The API will be available at:

```text
http://127.0.0.1:5001
```

When the app starts, it creates the SQLite database and adds default categories:

- Books
- Clothes
- Phones
- For home
- Other

## Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

The same response is also available at:

```http
GET /
```

## Swagger Documentation

Swagger UI is available at:

```text
http://127.0.0.1:5001/docs
```

OpenAPI JSON is available at:

```text
http://127.0.0.1:5001/openapi.json
```

## Run with Docker

Build the image:

```bash
docker build -t ecom-store-api .
```

Run the container:

```bash
docker run --rm -p 5001:5001 ecom-store-api
```

Check that the app works:

```text
http://127.0.0.1:5001/health
```

If Docker Hub is not available, but you already have a local Python base image, you can override the base image:

```bash
docker build --build-arg BASE_IMAGE=test_app_base:latest -t ecom-store-api .
```

## Run the Client

Start the API first:

```bash
.venv/bin/python app/routes.py
```

Then run the client in another terminal:

```bash
.venv/bin/python client.py
```

The client sends requests to:

- `GET /health`
- `GET /categories`
- `GET /goods`

## Seed Default Goods

Run this command to add several goods for every category:

```bash
.venv/bin/python seed_data.py
```

The seed script is safe to run more than once. Existing goods are skipped by name.

## Good

Example good:

```json
{
  "id": 1,
  "name": "IPhone",
  "price": 500.0,
  "category_id": 3
}
```

The database creates the `id`.

The `category_id` must point to an existing category.

## Category

Example category:

```json
{
  "category_id": 3,
  "name": "Phones"
}
```

## API Endpoints

### Get Health Status

```http
GET /health
```

### Get Swagger UI

```http
GET /docs
```

### Get OpenAPI JSON

```http
GET /openapi.json
```

### Get All Goods

```http
GET /goods
```

### Create a Good

```http
POST /goods
```

Body:

```json
{
  "name": "Phone",
  "price": 500,
  "category_id": 3
}
```

### Get a Good by ID

```http
GET /goods/1
```

### Update a Good

```http
PUT /goods/1
```

Body:

```json
{
  "name": "Updated phone",
  "price": 600,
  "category_id": 3
}
```

### Delete a Good

```http
DELETE /goods/1
```

### Get All Categories

```http
GET /categories
```

### Create a Category

```http
POST /categories
```

Body:

```json
{
  "name": "Laptops"
}
```

### Get Goods by Category

```http
GET /categories/3/goods
```

## Validation

Data is validated in `app/schemas.py`.

For goods:

- `name` is required
- `name` must be at least 2 characters long
- `price` is required
- `price` cannot be less than 0
- `category_id` is required
- `category_id` must be greater than 0

For categories:

- `name` is required
- `name` must be at least 2 characters long

## Logging

Logging is configured in `app/logger_config.py`.

The app logs:

- database initialization
- created goods and categories
- updated and deleted goods
- validation errors
- duplicate records
- not found responses
- health check requests

Example log format:

```text
2026-06-29 10:00:00 | INFO | routes | GET /health returned ok
```

## Run Tests

```bash
.venv/bin/python -m unittest discover -s test -v
```

Tests use a temporary SQLite database and do not change the main database file.

## What the Tests Check

- health check
- Swagger UI
- OpenAPI JSON specification
- getting all categories
- creating a category
- duplicate category error
- creating a good
- wrong good data error
- unknown category error
- duplicate good error
- getting all goods
- getting a good by `id`
- unknown good error
- updating a good
- deleting a good
- getting goods by category
- seeding default goods
