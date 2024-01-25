import json

from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post("/store/test_store", data={"name": "test_store", "items": []})

                self.assertEqual(response.status_code, 201, "")
                self.assertIsNotNone(StoreModel.find_by_name("test_store"))
                self.assertDictEqual(json.loads(response.data), {"id": 1, "name": "test_store", "items": []})

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test_store", data={"name": "test_store", "items": []})
                response = client.post("/store/test_store", data={"name": "test_store", "items": []})

                self.assertEqual(response.status_code, 400, "")
                self.assertDictEqual(json.loads(response.data), {'message': "A store with name 'test_store' already "
                                                                            "exists."})

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                post_response = client.post("/store/test_store", data={"name": "test_store", "items": []})

                self.assertEqual(post_response.status_code, 201, "")

                delete_response = client.delete("/store/test_store")

                self.assertEqual(delete_response.status_code, 200, "")
                self.assertIsNone(StoreModel.find_by_name("test_store"))
                self.assertDictEqual(json.loads(delete_response.data), {'message': 'Store deleted'})

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()

                get_response = client.get("/store/test_store")

                self.assertEqual(get_response.status_code, 200, "")
                self.assertDictEqual(json.loads(get_response.data), {"id": 1, "name": "test_store", "items": []})

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                get_response = client.get("/store/test_store")

                self.assertEqual(get_response.status_code, 404, "")
                self.assertDictEqual(json.loads(get_response.data), {'message': 'Store not found'})

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                ItemModel("test_item", 20, 1).save_to_db()

                resp = client.get("/store/test_store")
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data),
                                     {"id": 1, "name": "test_store", "items": [{"name": "test_item", "price": 20.0}]})

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()

                resp = client.get("/stores")
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {"stores": [{"id": 1, "name": "test_store", "items": []}]})

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                ItemModel("test_item", 20, 1).save_to_db()

                resp = client.get("/stores")
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data),
                                     {"stores": [{"id": 1, "name": "test_store", "items": [{"name": "test_item", "price": 20.0}]}]})
