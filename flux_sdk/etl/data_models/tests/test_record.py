import unittest
from datetime import datetime

from flux_sdk.etl.data_models.record import Record


class TestRecord(unittest.TestCase):
    def test_validate_empty(self):
        with self.assertRaises(TypeError):
            Record()  # intentionally empty

    def test_validate_primary_key_empty(self):
        for value in [None, ""]:
            with self.assertRaises(ValueError):
                Record(primary_key=value, fields={"some_field": "hello world"})

    def test_validate_primary_key_wrong_type(self):
        for value in [123, ("foo", "bar"), datetime.now()]:
            with self.assertRaises(TypeError):
                Record(primary_key=value, fields={"some_field": "hello world"})

    def test_validate_fields_empty(self):
        with self.assertRaises(ValueError):
            Record(primary_key="record_1", fields=None)

    def test_validate_fields_wrong_type(self):
        for value in [123, ("foo", "bar"), datetime.now()]:
            with self.assertRaises(TypeError):
                Record(primary_key="record_1", fields=value)

    def test_validate_references_wrong_type(self):
        for value in [123, ("foo", "bar"), datetime.now()]:
            with self.assertRaises(TypeError):
                Record(primary_key="record_1", fields={"foo": "bar"}, references=value)

    def test_validate_checkpoint_wrong_type(self):
        for value in [True, ("foo", "bar")]:
            with self.assertRaises(TypeError):
                Record(primary_key="record_1", fields={"foo": "bar"}, checkpoint=value)

    def test_validate_drop_wrong_type(self):
        for value in [123, ("foo", "bar"), {"foo": "bar"}, "hello world"]:
            with self.assertRaises(TypeError):
                Record(primary_key="record_1", fields={"foo": "bar"}, drop=value)

    def test_validate_success_minimal(self):
        Record(primary_key="record_1", fields={"some_field": "hello world"})

    def test_validate_success_complete(self):
        Record(
            primary_key="record_1",
            fields={"some_field": "hello world"},
            references={"other_object_id": "other_object_1"},
            checkpoint=datetime.now(),
            drop=False,
        )


if __name__ == '__main__':
    unittest.main()
