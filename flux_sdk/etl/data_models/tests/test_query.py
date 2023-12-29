import unittest
from datetime import datetime

from flux_sdk.etl.data_models.query import MongoQuery, SQLQuery


class TestSQLQuery(unittest.TestCase):
    def test_validate_empty(self):
        with self.assertRaises(TypeError):
            SQLQuery()  # intentionally empty

    def test_validate_text_empty(self):
        for value in [None, ""]:
            with self.assertRaises(ValueError):
                SQLQuery(text=value)

    def test_validate_text_wrong_type(self):
        for value in [123, ("foo", "bar"), datetime.now()]:
            with self.assertRaises(TypeError):
                SQLQuery(text=value)

    def test_validate_args_wrong_type(self):
        for value in [123, "foo", ("foo", "bar"), datetime.now()]:
            with self.assertRaises(TypeError):
                SQLQuery(text="select column from table", args=value)

    def test_validate_success_minimal(self):
        SQLQuery(text="select column from table")

    def test_validate_success_complete(self):
        SQLQuery(
            text="select column from table where id = @id",
            args={"id": "record_1"},
        )


class TestMongoQuery(unittest.TestCase):
    def test_validate_empty(self):
        with self.assertRaises(TypeError):
            MongoQuery()  # intentionally empty

    def test_validate_collection_empty(self):
        for value in [None, ""]:
            with self.assertRaises(ValueError):
                MongoQuery(collection=value)

    def test_validate_collection_wrong_type(self):
        for value in [123, ("foo", "bar"), datetime.now()]:
            with self.assertRaises(TypeError):
                MongoQuery(collection=value)

    def test_validate_filter_wrong_type(self):
        for value in [123, ("foo", "bar"), datetime.now()]:
            with self.assertRaises(TypeError):
                MongoQuery(collection="some_collection", filter=value)

    def test_validate_projection_wrong_type(self):
        for value in [123, ("foo", "bar"), datetime.now()]:
            with self.assertRaises(TypeError):
                MongoQuery(collection="some_collection", projection=value)

    def test_validate_aggregate_wrong_type(self):
        for value in [123, ["AnyObject"], ("foo", "bar"), datetime.now()]:
            with self.assertRaises(TypeError):
                MongoQuery(collection="some_collection", aggregate=value)

    def test_validate_success_minimal(self):
        MongoQuery(collection="some_collection")

    def test_validate_success_complete(self):
        MongoQuery(
            collection="some_collection",
            filter={"id": "record_1"},
            aggregate=[
                {"foo": "bar"},
            ],
        )


if __name__ == '__main__':
    unittest.main()
