# Tests

This folder contains unit tests for the E-commerce Store API.

The tests use:

- `unittest`
- Flask `test_client`
- temporary SQLite database

## Test File

```text
test_routes.py
```

This file checks the API routes from `routes.py`.

## Run Tests

Run this command from the project root:

```bash
.venv/bin/python -m unittest discover -s test -v
```

Project root:

```bash
cd /Users/billcarter/Documents/my_project/ecom_store
```

## Why Temporary Database Is Used

Each test creates a temporary SQLite database.

This means tests do not change the main `store.db` file.

In `setUp()`:

```python
self.temp_dir = tempfile.TemporaryDirectory()
models.DATABASE = os.path.join(self.temp_dir.name, 'test_store.db')
models.init_db()
```

In `tearDown()`:

```python
self.temp_dir.cleanup()
```

So every test starts with a clean database.

## What Is Tested

Categories:

- get all categories
- create a category
- return an error for duplicate category

Goods:

- create a good
- return validation errors for wrong data
- return an error for unknown category
- return an error for duplicate good
- get all goods
- get one good by `id`
- return an error for unknown good
- update a good
- delete a good
- get goods by category

## Main Test Class

```python
class StoreApiTestCase(unittest.TestCase):
```

This class contains all API tests.

`setUp()` runs before every test.

`tearDown()` runs after every test.

## Helper Method

```python
def create_good(self, name='Test phone', price=100, category_id=3):
```

This helper creates a test good and keeps the tests shorter.

Example:

```python
self.create_good(name='Phone', category_id=3)
```

## Expected Result

If everything works, the test result should end with:

```text
Ran 13 tests

OK
```
