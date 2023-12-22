import unittest
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional, Union

from flux_sdk.flux_core.validation import check_field

Checkpoint = Union[str, int, datetime]


class TestCheckField(unittest.TestCase):
    def test_required_string_value(self):
        @dataclass
        class Object:
            required_string_value: str

        o = Object(required_string_value="hello world")
        check_field(o, "required_string_value", str, required=True)

        # check empty values
        for value in [None, ""]:
            o.required_string_value = value
            with self.assertRaises(ValueError):
                check_field(o, "required_string_value", str, required=True)

        # check type
        for value in [123, datetime.now(), {"hello": "world"}, ("foo", "bar", "baz")]:
            o.required_string_value = value
            with self.assertRaises(TypeError):
                check_field(o, "required_string_value", str, required=True)

    def test_optional_string_value(self):
        @dataclass
        class Object:
            optional_string_value: Optional[str] = None

        o = Object()
        check_field(o, "optional_string_value", str)

        # check type
        for value in [123, datetime.now(), {"hello": "world"}, ("foo", "bar", "baz")]:
            o.optional_string_value = value
            with self.assertRaises(TypeError):
                check_field(o, "optional_string_value", str)

    def test_required_union_type(self):
        @dataclass
        class Record:
            checkpoint: Checkpoint

        r = Record(checkpoint=None)
        with self.assertRaises(ValueError):
            check_field(r, "checkpoint", Checkpoint, required=True)

        # valid types
        for value in ["hello world", 123, datetime.now()]:
            r.checkpoint = value
            check_field(r, "checkpoint", Checkpoint, required=True)

        # invalid types
        for value in [True, ("foo", "bar", "baz"), {"hello": "world"}]:
            r.checkpoint = value
            with self.assertRaises(TypeError):
                check_field(r, "checkpoint", Checkpoint, required=True)

    def test_dict_strings(self):
        @dataclass
        class Record:
            references: dict[str, str]

        r = Record(references=None)

        # optional
        check_field(r, "references", dict[str, str])

        # required
        with self.assertRaises(ValueError):
            check_field(r, "references", dict[str, str], required=True)

        # valid type
        r.references = {"hello": "world"}
        check_field(r, "references", dict[str, str])
        check_field(r, "references", dict[str, str], required=True)

        # invalid types
        for value in ["hello world", 123, 3.14, True, {"hello": 123}]:
            r.references = value
            with self.assertRaises(TypeError):
                check_field(r, "references", dict[str, str])
                check_field(r, "references", dict[str, str], required=True)

    def test_dict_any(self):
        @dataclass
        class Record:
            references: dict[Any, Any]

        r = Record(references=None)

        # optional
        check_field(r, "references", dict[Any, Any])

        # valid type
        r.references = {"hello": "world", 123: True}
        check_field(r, "references", dict[Any, Any])
        check_field(r, "references", dict[Any, Any], required=True)



if __name__ == '__main__':
    unittest.main()
