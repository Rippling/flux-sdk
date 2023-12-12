import datetime
import unittest

from pydantic import ValidationError

from flux_sdk.etl.data_models.record import Record


class TestRecord(unittest.TestCase):
    def test_validate_empty(self):
        with self.assertRaises(ValidationError):
            Record()  # intentionally empty

    def test_validate_primary_key_wrong_type(self):
        with self.assertRaises(ValidationError):
            Record(
                primary_key=123,  # intentionally int rather than string
                fields={"some_field": "hello world"},
            )

    def test_validate_success_minimal(self):
        Record(
            primary_key="record_1",
            fields={"some_field": "hello world"},
        )

    def test_validate_success_complete(self):
        Record(
            primary_key="record_1",
            fields={"some_field": "hello world"},
            references={"other_object_id": "other_object_1"},
            checkpoint=datetime.datetime.now(),
            drop=False,
        )


if __name__ == '__main__':
    unittest.main()
