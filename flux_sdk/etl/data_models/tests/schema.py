import unittest

from pydantic import ValidationError

from flux_sdk.etl.data_models.schema import Schema, SchemaField, SchemaDataType, EmployeeReference, EmployeeLookup, CustomObjectReference


class TestSchema(unittest.TestCase):
    def test_validate_empty(self):
        with self.assertRaises(ValidationError):
            Schema()  # intentionally empty

    def test_validate_name_wrong_type(self):
        with self.assertRaises(ValidationError):
            Schema(
                name=123,  # intentionally int rather than string
                category_name="some_category",
                primary_key_field="id",
                fields=[
                    SchemaField(name="some_field", data_type=SchemaDataType.String),
                ]
            )

    def test_validate_success_minimal(self):
        Schema(
            name="some_object",
            category_name="some_category",
            primary_key_field="id",
            fields=[
                SchemaField(name="some_field", data_type=SchemaDataType.String),
            ]
        )

    def test_validate_success_complete(self):
        Schema(
            name="some_object",
            description="This is a description of an object.",
            category_name="some_category",
            category_description="This is a description of a category.",
            primary_key_field="id",
            name_field="name",
            created_date_field="created_date",
            last_modified_date_field="last_modified_date",
            owner=EmployeeReference(
                lookup=EmployeeLookup.EMPLOYEE_ID,
                description="This is a description of how some_object is related to Employee.",
            ),
            fields=[
                SchemaField(
                    name="some_field",
                    data_type=SchemaDataType.String,
                    description="This is a description of some_field.",
                    is_required=False,
                    is_unique=False,
                ),
            ],
            references={
                "another_object_id": CustomObjectReference(
                    object="another_object",
                    lookup="id",
                    description="This is a description of another_object in the context of some_object.",
                ),
            },
        )


if __name__ == '__main__':
    unittest.main()
