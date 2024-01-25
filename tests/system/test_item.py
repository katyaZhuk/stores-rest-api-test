import json

from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest


class TestItem(BaseTest):
    def setUp(self):
        super(TestItem, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '123456').save_to_db()
                auth_request = client.post('/auth', data=json.dumps({
                    'username': 'test',
                    'password': '123456'
                }), headers={'Content-Type': 'application/json'})
                self.auth_header = "JWT {}".format(json.loads(auth_request.data)['access_token'])

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get("/item/test")

                self.assertEqual(resp.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get("/item/test",
                                  headers={"Authorization": self.auth_header})
                self.assertEqual(404, resp.status_code)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                ItemModel("test_item", 20, 1).save_to_db()
                resp = client.get("/item/test_item",
                                  headers={"Authorization": self.auth_header})
                self.assertEqual(200, resp.status_code)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                ItemModel("test_item", 20, 1).save_to_db()
                resp = client.delete("/item/test_item")

                self.assertEqual(200, resp.status_code)
                self.assertEqual({'message': 'Item deleted'}, json.loads(resp.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                resp = client.post("/item/test_item", data={"price": 20.0, "store_id": 1})

                self.assertEqual(201, resp.status_code)
                self.assertDictEqual({"name": "test_item", "price": 20.0}, json.loads(resp.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                ItemModel("test_item", 20, 1).save_to_db()
                resp = client.post("/item/test_item", data={"name": "test_item", "price": 20.0, "store_id": 1})

                self.assertEqual(400, resp.status_code)
                self.assertDictEqual({'message': "An item with name 'test_item' already exists."},
                                     json.loads(resp.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                resp = client.put("/item/test_item", data={"name": "test_item", "price": 25.0, "store_id": 1})

                self.assertEqual(200, resp.status_code)
                self.assertDictEqual({"name": "test_item", "price": 25.0},
                                     json.loads(resp.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                ItemModel("test_item", 20, 1).save_to_db()
                resp = client.put("/item/test_item", data={"name": "test_item", "price": 25.0, "store_id": 1})

                self.assertEqual(200, resp.status_code)
                self.assertDictEqual({"name": "test_item", "price": 25.0},
                                     json.loads(resp.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                ItemModel("test_item", 20, 1).save_to_db()

                resp = client.get("/items")

                self.assertEqual(200, resp.status_code)
                self.assertDictEqual({"items": [{"name": "test_item", "price": 20.0}]},
                                     json.loads(resp.data))
