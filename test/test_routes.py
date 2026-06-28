import os
import sys
import tempfile
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

import models
from routes import app


class StoreApiTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        models.DATABASE = os.path.join(self.temp_dir.name, 'test_store.db')

        models.init_db()

        app.config['TESTING'] = True
        self.client = app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_good(self, name='Test phone', price=100, category_id=3):
        return self.client.post(
            '/goods',
            json={
                'name': name,
                'price': price,
                'category_id': category_id,
            }
        )

    def test_get_categories(self):
        response = self.client.get('/categories')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 5)
        self.assertEqual(response.json[0]['name'], 'Books')

    def test_create_category(self):
        response = self.client.post('/categories', json={'name': 'Laptops'})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Laptops')
        self.assertIn('category_id', response.json)

    def test_create_duplicate_category(self):
        self.client.post('/categories', json={'name': 'Laptops'})
        response = self.client.post('/categories', json={'name': 'Laptops'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json['message'],
            'Category with this name already exists'
        )

    def test_create_good(self):
        response = self.create_good()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Test phone')
        self.assertEqual(response.json['price'], 100.0)
        self.assertEqual(response.json['category_id'], 3)
        self.assertIn('id', response.json)

    def test_create_good_with_wrong_data(self):
        response = self.client.post(
            '/goods',
            json={
                'name': 'A',
                'price': -10,
                'category_id': 0,
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.json)
        self.assertIn('price', response.json)
        self.assertIn('category_id', response.json)

    def test_create_good_with_unknown_category(self):
        response = self.create_good(category_id=999)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'Category not found')

    def test_create_duplicate_good(self):
        self.create_good()
        response = self.create_good()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json['message'],
            'Good with this name already exists'
        )

    def test_get_goods(self):
        self.create_good(name='Phone')
        self.create_good(name='Book', price=20, category_id=1)

        response = self.client.get('/goods')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

    def test_get_good_by_id(self):
        created_good = self.create_good()
        good_id = created_good.json['id']

        response = self.client.get(f'/goods/{good_id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], good_id)
        self.assertEqual(response.json['name'], 'Test phone')

    def test_get_unknown_good(self):
        response = self.client.get('/goods/999')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'Good not found')

    def test_update_good(self):
        created_good = self.create_good()
        good_id = created_good.json['id']

        response = self.client.put(
            f'/goods/{good_id}',
            json={
                'name': 'Updated phone',
                'price': 200,
                'category_id': 3,
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], good_id)
        self.assertEqual(response.json['name'], 'Updated phone')
        self.assertEqual(response.json['price'], 200.0)

    def test_delete_good(self):
        created_good = self.create_good()
        good_id = created_good.json['id']

        delete_response = self.client.delete(f'/goods/{good_id}')
        get_response = self.client.get(f'/goods/{good_id}')

        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(delete_response.json['message'], 'Good deleted')
        self.assertEqual(get_response.status_code, 404)

    def test_get_goods_by_category(self):
        self.create_good(name='Phone', category_id=3)
        self.create_good(name='Book', price=20, category_id=1)

        response = self.client.get('/categories/3/goods')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['name'], 'Phone')


if __name__ == '__main__':
    unittest.main()
