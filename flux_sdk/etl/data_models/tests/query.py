import unittest

from pydantic import ValidationError

from flux_sdk.etl.data_models.query import SQLQuery, MongoQuery


class TestSQLQuery(unittest.TestCase):
    def test_validate_empty(self):
        with self.assertRaises(ValidationError):
            SQLQuery()  # intentionally empty

    def test_validate_text_wrong_type(self):
        with self.assertRaises(ValidationError):
            SQLQuery(
                text=123,  # intentionally int rather than string
            )

    def test_validate_success_minimal(self):
        SQLQuery(
            text="select column from table",
        )

    def test_validate_success_complete(self):
        SQLQuery(
            text="select column from table where id = @id",
            args={"id": "record_1"},
        )


class TestMongoQuery(unittest.TestCase):
    def test_validate_empty(self):
        with self.assertRaises(ValidationError):
            MongoQuery()  # intentionally empty

    def test_validate_collection_wrong_type(self):
        with self.assertRaises(ValidationError):
            MongoQuery(
                collection=123,  # intentionally int rather than string
            )

    def test_validate_success_minimal(self):
        MongoQuery(
            collection="some_collection",
        )

    def test_validate_success_complete(self):
        MongoQuery(
            collection="some_collection",
            filter={"id": "record_1"},
        )


if __name__ == '__main__':
    unittest.main()
