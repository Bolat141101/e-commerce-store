# E-commerce Store API

A small learning REST API for an e-commerce store.

The project uses a simple Python stack:

- `Flask`
- `flask_restful`
- `sqlite3`
- `dataclasses`
- `marshmallow`
- `unittest`

## Features

- get all goods
- get one good by `id`
- create a good
- update a good
- delete a good
- get all categories
- create a category
- get goods by category

## Project Structure

```text
ecom_store/
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── models.py
├── schemas.py
├── routes.py
├── store.db
├── test/
│   └── test_routes.py
└── README.md
```

## File Responsibilities

`models.py` works with the SQLite database.

`schemas.py` validates incoming data with `marshmallow`.

`routes.py` contains Flask routes and starts the application.

`test/test_routes.py` contains unit tests for the API.

## Run the Project

Go to the project folder:

```bash
cd /Users/billcarter/Documents/my_project/ecom_store
```

Start the server:

```bash
.venv/bin/python routes.py
```

After starting the server, the API will be available at:

```text
http://127.0.0.1:5000
```

When the app starts, it creates the `store.db` database and adds default categories:

- Books
- Clothes
- Phones
- For home
- Other

## Run with Docker

Build the image:

```bash
docker build -t ecom-store-api .
```

Run the container:

```bash
docker run --rm -p 5000:5000 ecom-store-api
```

Then open:

```text
http://127.0.0.1:5000/categories
```

If Docker Hub is not available, but you already have a local Python base image, you can override the base image:

```bash
docker build --build-arg BASE_IMAGE=test_app_base:latest -t ecom-store-api .
```

## Good

Example good:

```json
{
  "id": 1,
  "name": "Phone",
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

Data is validated in `schemas.py`.

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

## Run Tests

```bash
.venv/bin/python -m unittest discover -s test -v
```

Tests use a temporary SQLite database and do not change the main `store.db` file.

## What the Tests Check

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
