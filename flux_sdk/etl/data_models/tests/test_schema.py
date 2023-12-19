import unittest
from datetime import datetime

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

    def test_validate_name_empty(self):
        for value in [None, ""]:
            with self.assertRaises(ValueError):
                Schema(
                    name=value,
                    category_name="some_category",
                    category_description="This is a description.",
                    primary_key_field="id",
                    name_field="name",
                    fields=[
                        SchemaField(name="some_field", data_type=SchemaDataType.String),
                    ]
                )

    def test_validate_name_wrong_type(self):
        for value in [123, ("foo", "bar"), datetime.now()]:
            with self.assertRaises(TypeError):
                Schema(
                    name=value,
                    category_name="some_category",
                    category_description="This is a description.",
                    primary_key_field="id",
                    name_field="name",
                    fields=[
                        SchemaField(name="some_field", data_type=SchemaDataType.String),
                    ]
                )

    def test_validate_category_name_empty(self):
        for value in [None, ""]:
            with self.assertRaises(ValueError):
                Schema(
                    name="some_object",
                    category_name=value,
                    category_description="This is a description.",
                    primary_key_field="id",
                    name_field="name",
                    fields=[
                        SchemaField(name="some_field", data_type=SchemaDataType.String),
                    ]
                )

    def test_validate_category_name_wrong_type(self):
        for value in [123, ("foo", "bar"), datetime.now()]:
            with self.assertRaises(TypeError):
                Schema(
                    name="some_object",
                    category_name=value,
                    category_description="This is a description.",
                    primary_key_field="id",
                    name_field="name",
                    fields=[
                        SchemaField(name="some_field", data_type=SchemaDataType.String),
                    ]
                )

    def test_validate_category_description_empty(self):
        for value in [None, ""]:
            with self.assertRaises(ValueError):
                Schema(
                    name="some_object",
                    category_name="some_category",
                    category_description=value,
                    primary_key_field="id",
                    name_field="name",
                    fields=[],
                )

    def test_validate_category_description_wrong_type(self):
        for value in [123, ("foo", "bar"), datetime.now()]:
            with self.assertRaises(TypeError):
                Schema(
                    name="some_object",
                    category_name="some_category",
                    category_description=value,
                    primary_key_field="id",
                    name_field="name",
                    fields=[],
                )

    def test_validate_primary_key_field_empty(self):
        for value in [None, ""]:
            with self.assertRaises(ValueError):
                Schema(
                    name="some_object",
                    category_name="some_category",
                    category_description="This is a description.",
                    primary_key_field=value,
                    name_field="name",
                    fields=[
                        SchemaField(name="some_field", data_type=SchemaDataType.String),
                    ]
                )

    def test_validate_primary_key_field_wrong_type(self):
        for value in [123, ("foo", "bar"), datetime.now()]:
            with self.assertRaises(TypeError):
                Schema(
                    name="some_object",
                    category_name="some_category",
                    category_description="This is a description.",
                    primary_key_field=value,
                    name_field="name",
                    fields=[
                        SchemaField(name="some_field", data_type=SchemaDataType.String),
                    ],
                )

    def test_validate_name_field_empty(self):
        for value in [None, ""]:
            with self.assertRaises(ValueError):
                Schema(
                    name="some_object",
                    category_name="some_category",
                    category_description="This is a description.",
                    primary_key_field="id",
                    name_field=value,
                    fields=[
                        SchemaField(name="some_field", data_type=SchemaDataType.String),
                    ]
                )

    def test_validate_name_field_wrong_type(self):
        for value in [123, ("foo", "bar"), datetime.now()]:
            with self.assertRaises(TypeError):
                Schema(
                    name="some_object",
                    category_name="some_category",
                    category_description="This is a description.",
                    primary_key_field="id",
                    name_field=value,
                    fields=[
                        SchemaField(name="some_field", data_type=SchemaDataType.String),
                    ]
                )

    def test_validate_fields_wrong_type(self):
        for value in [123, ("foo", "bar"), datetime.now()]:
            with self.assertRaises(TypeError):
                Schema(
                    name="some_object",
                    category_name="some_category",
                    category_description="This is a description.",
                    primary_key_field="id",
                    name_field="name",
                    fields=value,
                )

    def test_validate_description_wrong_type(self):
        for value in [123, ("foo", "bar"), datetime.now()]:
            with self.assertRaises(TypeError):
                Schema(
                    name="some_object",
                    category_name="some_category",
                    category_description="This is a description.",
                    primary_key_field="id",
                    name_field="name",
                    fields=[],
                    description=value,
                )

    def test_validate_created_date_field_wrong_type(self):
        for value in [123, ("foo", "bar"), datetime.now()]:
            with self.assertRaises(TypeError):
                Schema(
                    name="some_object",
                    category_name="some_category",
                    category_description="This is a description.",
                    primary_key_field="id",
                    name_field="name",
                    fields=[],
                    created_date_field=value,
                )

    def test_validate_last_modified_date_field_wrong_type(self):
        for value in [123, ("foo", "bar"), datetime.now()]:
            with self.assertRaises(TypeError):
                Schema(
                    name="some_object",
                    category_name="some_category",
                    category_description="This is a description.",
                    primary_key_field="id",
                    name_field="name",
                    fields=[],
                    last_modified_date_field=value,
                )

    def test_validate_references_wrong_type(self):
        for value in [123, ("foo", "bar"), datetime.now()]:
            with self.assertRaises(TypeError):
                Schema(
                    name="some_object",
                    category_name="some_category",
                    category_description="This is a description.",
                    primary_key_field="id",
                    name_field="name",
                    fields=[],
                    references=value,
                )

    def test_validate_owner_wrong_type(self):
        for value in [123, "foo bar", datetime.now()]:
            with self.assertRaises(TypeError):
                Schema(
                    name="some_object",
                    category_name="some_category",
                    category_description="This is a description.",
                    primary_key_field="id",
                    name_field="name",
                    fields=[],
                    owner=value,
                )

    def test_validate_success_minimal(self):
        Schema(
            name="some_object",
            category_name="some_category",
            category_description="This is a description.",
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
            fields=[
                SchemaField(
                    name="some_field",
                    data_type=SchemaDataType.String,
                    description="This is a description of some_field.",
                    is_required=False,
                    is_unique=False,
                ),
            ],
            owner=(
                "owner",
                EmployeeReference(
                    lookup=EmployeeLookup.EMPLOYEE_ID,
                    description="This is a description of how some_object is related to Employee.",
                )
            ),
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

    def test_validate_name_empty(self):
        for value in [None, ""]:
            with self.assertRaises(ValueError):
                SchemaField(name=value, data_type=SchemaDataType.LongText)

    def test_validate_name_wrong_type(self):
        for value in [123, ("foo", "bar"), {"foo": "bar"}, datetime.now()]:
            with self.assertRaises(TypeError):
                SchemaField(name=value, data_type=SchemaDataType.LongText)

    def test_validate_data_type_empty(self):
        for value in [None, ""]:
            with self.assertRaises(ValueError):
                SchemaField(name="some_object", data_type=value)

    def test_validate_data_type_wrong_type(self):
        for value in [123, ("foo", "bar"), {"foo": "bar"}, datetime.now()]:
            with self.assertRaises(TypeError):
                SchemaField(name="some_object", data_type=value)

    def test_validate_data_type_not_valid_enum_value(self):
        with self.assertRaises(TypeError):
            SchemaField(
                name="some_field",
                data_type="not one of the valid enums",
            )

    def test_validate_description_wrong_type(self):
        for value in [123, ("foo", "bar"), {"foo": "bar"}, datetime.now()]:
            with self.assertRaises(TypeError):
                SchemaField(name="some_object", data_type=SchemaDataType.String, description=value)

    def test_validate_is_required_wrong_type(self):
        for value in [123, ("foo", "bar"), {"foo": "bar"}, datetime.now()]:
            with self.assertRaises(TypeError):
                SchemaField(name="some_object", data_type=SchemaDataType.String, is_required=value)

    def test_validate_is_unique_wrong_type(self):
        for value in [123, ("foo", "bar"), {"foo": "bar"}, datetime.now()]:
            with self.assertRaises(TypeError):
                SchemaField(name="some_object", data_type=SchemaDataType.String, is_unique=value)

    def test_validate_enum_values_wrong_type(self):
        for value in [123, ("foo", "bar"), {"foo": "bar"}, datetime.now()]:
            with self.assertRaises(TypeError):
                SchemaField(name="some_object", data_type=SchemaDataType.Enum, enum_values=value)

    def test_validate_enum_restricted_wrong_type(self):
        for value in [123, ("foo", "bar"), {"foo": "bar"}, datetime.now()]:
            with self.assertRaises(TypeError):
                SchemaField(name="some_object", data_type=SchemaDataType.Enum, enum_restricted=value)

    def test_validate_enum_without_values(self):
        with self.assertRaises(ValueError):
            SchemaField(name="some_object", data_type=SchemaDataType.Enum, enum_values=[])
            SchemaField(name="some_object", data_type=SchemaDataType.MultiEnum, enum_values=[])

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

    def test_validate_object_empty(self):
        for value in [None, ""]:
            with self.assertRaises(ValueError):
                CustomObjectReference(object=value, lookup="some_field")

    def test_validate_object_wrong_type(self):
        for value in [123, ("foo", "bar"), {"foo": "bar"}, datetime.now()]:
            with self.assertRaises(TypeError):
                CustomObjectReference(object=value, lookup="some_field")

    def test_validate_lookup_empty(self):
        for value in [None, ""]:
            with self.assertRaises(ValueError):
                CustomObjectReference(object="some_object", lookup=value)

    def test_validate_lookup_wrong_type(self):
        for value in [123, ("foo", "bar"), {"foo": "bar"}, datetime.now()]:
            with self.assertRaises(TypeError):
                CustomObjectReference(object="some_object", lookup=value)

    def test_validate_description_wrong_type(self):
        for value in [123, ("foo", "bar"), {"foo": "bar"}, datetime.now()]:
            with self.assertRaises(TypeError):
                CustomObjectReference(object="some_object", lookup="some_field", description=value)

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

    def test_validate_lookup_empty(self):
        for value in [None, ""]:
            with self.assertRaises(ValueError):
                EmployeeReference(lookup=value)

    def test_validate_lookup_wrong_type(self):
        for value in [123, ("foo", "bar"), {"foo": "bar"}, datetime.now()]:
            with self.assertRaises(TypeError):
                EmployeeReference(lookup=value)

    def test_validate_description_wrong_type(self):
        for value in [123, ("foo", "bar"), {"foo": "bar"}, datetime.now()]:
            with self.assertRaises(TypeError):
                EmployeeReference(lookup=EmployeeLookup.EMPLOYEE_ID, description=value)

    def test_validate_success_minimal(self):
        EmployeeReference(lookup=EmployeeLookup.EMPLOYEE_ID)

    def test_validate_success_complete(self):
        EmployeeReference(
            lookup=EmployeeLookup.WORK_EMAIL,
            description="This is a description of the reference.",
        )


if __name__ == '__main__':
    unittest.main()
