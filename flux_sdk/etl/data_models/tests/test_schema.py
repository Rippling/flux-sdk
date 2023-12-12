import unittest

from pydantic import ValidationError

from flux_sdk.etl.data_models.schema import (
    CustomObjectReference,
    EmployeeLookup,
    EmployeeReference,
    Schema,
    SchemaDataType,
    SchemaField,
)


class TestSchema(unittest.TestCase):
    def test_validate_empty(self):
        with self.assertRaises(TypeError):
            Schema()  # intentionally empty

    def test_validate_name_wrong_type(self):
        with self.assertRaises(ValidationError):
            Schema(
                name=("foo", "bar"),  # intentionally wrong type
                category_name="some_category",
                primary_key_field="id",
                name_field="name",
                fields=[
                    SchemaField(name="some_field", data_type=SchemaDataType.String),
                ]
            )

    def test_validate_success_minimal(self):
        Schema(
            name="some_object",
            category_name="some_category",
            primary_key_field="id",
            name_field="name",
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


class TestSchemaField(unittest.TestCase):
    def test_validate_empty(self):
        with self.assertRaises(TypeError):
            SchemaField()  # intentionally empty

    def test_validate_name_wrong_type(self):
        with self.assertRaises(ValidationError):
            SchemaField(
                name=("foo", "bar"),  # intentionally wrong type
                data_type=SchemaDataType.LongText,
            )

    def test_validate_data_type_not_valid_enum_value(self):
        with self.assertRaises(ValidationError):
            SchemaField(
                name="some_field",
                data_type="not one of the valid enums",
            )

    def test_validate_success_minimal(self):
        SchemaField(
            name="some_text_field",
            data_type=SchemaDataType.String,
        )

    def test_validate_success_complete(self):
        SchemaField(
            name="some_enum_field",
            data_type=SchemaDataType.Enum,
            description="This is a description for a field.",
            is_required=True,
            is_unique=False,
            enum_values=["A", "B", "C"],
            enum_restricted=True,
        )


class TestCustomObjectReference(unittest.TestCase):
    def test_validate_empty(self):
        with self.assertRaises(TypeError):
            CustomObjectReference()  # intentionally empty

    def test_validate_object_wrong_type(self):
        with self.assertRaises(ValidationError):
            CustomObjectReference(
                object=("foo", "bar"),  # intentionally wrong type
                lookup="some_field"
            )

    def test_validate_success_minimal(self):
        CustomObjectReference(
            object="some_object",
            lookup="some_field",
        )

    def test_validate_success_complete(self):
        CustomObjectReference(
            object="some_object",
            lookup="some_field",
            description="This is a description of the reference.",
        )


class TestEmployeeReference(unittest.TestCase):
    def test_validate_empty(self):
        with self.assertRaises(TypeError):
            EmployeeReference()  # intentionally empty

    def test_validate_lookup_wrong_type(self):
        with self.assertRaises(ValidationError):
            EmployeeReference(
                lookup=("foo", "bar"),  # intentionally wrong type
            )

    def test_validate_success_minimal(self):
        EmployeeReference(lookup=EmployeeLookup.EMPLOYEE_ID)

    def test_validate_success_complete(self):
        EmployeeReference(
            lookup=EmployeeLookup.BUSINESS_EMAIL,
            description="This is a description of the reference.",
        )


if __name__ == '__main__':
    unittest.main()
