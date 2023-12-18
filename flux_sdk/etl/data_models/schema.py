from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from flux_sdk.flux_core.validation import raise_if_missing_or_incorrect_type, raise_if_incorrect_type


# These are the data types supported by Rippling Custom Objects.
class SchemaDataType(Enum):
    Bool = "bool"
    Currency = "currency"
    Date = "date"
    DateTime = "datetime"
    Decimal = "decimal"
    Email = "email"
    Enum = "enum"
    Integer = "integer"
    LongText = "longtext"
    MultiEnum = "multienum"
    Percent = "percent"
    String = "string"
    Time = "time"
    Url = "url"


# A field usually corresponds to a column in a database, it is one datum within a Record.
@dataclass(kw_only=True)
class SchemaField:
    # This maps to the field name in the Rippling Custom Object.
    name: str

    # This indicates the data type used in the Rippling Custom Object.
    data_type: SchemaDataType

    # This is a longer explanation of the field that will appear in the Rippling Custom Object UI.
    description: Optional[str] = None

    # When enabled, this value will be required to be not empty by Rippling Custom Object.
    is_required: bool = False

    # When enabled, this value will be enforced as unique by Rippling Custom Object.
    is_unique: bool = False

    # When using an Enum data type, this indicates the possible values.
    enum_values: Optional[list[str]] = None

    # When using an Enum data type, this indicates if *only* enum_values are accepted, meaning anything else will be
    # rejected with an error.
    enum_restricted: bool = False

    # Perform validation.
    def __post_init__(self):
        raise_if_missing_or_incorrect_type(self, "name", str)
        raise_if_missing_or_incorrect_type(self, "data_type", SchemaDataType)
        raise_if_incorrect_type(self, "description", str)
        raise_if_incorrect_type(self, "enum_values", list)

        if not isinstance(self.is_required, bool):
            raise TypeError("is_required must be a bool")

        if not isinstance(self.is_unique, bool):
            raise TypeError("is_unique must be a bool")

        if not isinstance(self.enum_restricted, bool):
            raise TypeError("enum_restricted must be a bool")

        if self.data_type in [SchemaDataType.Enum, SchemaDataType.MultiEnum]:
            if len(self.enum_values) == 0:
                raise ValueError("enum_values must have at least 1 value")


# This allows creating a reference to an existing Custom Object.
@dataclass(kw_only=True)
class CustomObjectReference:
    # The name of the Custom Object to link to.
    object: str

    # The name of the field on the Custom Object to use for the link.
    lookup: str

    # An optional explanation for this reference to be shown in the Rippling Custom Object UI.
    description: Optional[str] = None

    # Perform validation.
    def __post_init__(self):
        raise_if_missing_or_incorrect_type(self, "object", str)
        raise_if_missing_or_incorrect_type(self, "lookup", str)
        raise_if_incorrect_type(self, "description", str)


# These are the available lookup-fields for a Rippling Employee.
class EmployeeLookup(Enum):
    # The Rippling Employee ID.
    EMPLOYEE_ID = "employee_id"

    # The personal email for a Rippling Employee.
    PERSONAL_EMAIL = "personal_email"

    # The work/business email for a Rippling Employee.
    WORK_EMAIL = "work_email"


# This allows creating a reference to a Rippling employee.
@dataclass(kw_only=True)
class EmployeeReference:
    # The name of the field on the Employee object to use for the link.
    lookup: EmployeeLookup

    # An optional explanation for this reference to be shown in the Rippling Custom Object UI.
    description: Optional[str] = None

    # Perform validation.
    def __post_init__(self):
        raise_if_missing_or_incorrect_type(self, "lookup", EmployeeLookup)
        raise_if_incorrect_type(self, "description", str)


# This lists the available types that can be used for schema references.
Reference = Union[CustomObjectReference, EmployeeReference]


# A schema describes the shape of an object being imported and is used by Rippling to define the Custom Object.
@dataclass(kw_only=True)
class Schema:
    # This is the name of the Custom Object.
    name: str

    # This is used to put this Custom Object into a group/category. If a category with this name already exists, a new
    # one will not be created.
    category_name: str

    # When creating a new group/category, this will set a description that will appear in the Rippling Custom Object UI.
    # If the category already exists, the description will be updated.
    category_description: str

    # This is the name of the field used for the record name, which is displayed in the Rippling Custom Object UI. When
    # not provided,
    name_field: str

    # These are the remaining data fields.
    fields: list[SchemaField]

    # This is the name of the field used for the primary key (aka: External ID).
    primary_key_field: Optional[str] = None

    # This is a more detailed explanation of the field which will appear in the Rippling Custom Object UI.
    description: Optional[str] = None

    # This is the name of the field that reflects when the record was first created. When a field name is not provided,
    # Rippling will use the time that the record is first imported.
    created_date_field: Optional[str] = None

    # This is the name of the field that reflects when the record was last updated. When a field name is not provided,
    # Rippling will use the time that the record was last updated.
    last_modified_date_field: Optional[str] = None

    # These are the links to other objects. The keys are the field names that should be the origin for the link/edge.
    references: Optional[dict[str, Reference]] = None

    # This establishes the built-in link to Employee, if applicable.
    owner: Optional[tuple[str, EmployeeReference]] = None

    # Perform validation.
    def __post_init__(self):
        raise_if_missing_or_incorrect_type(self, "name", str)
        raise_if_missing_or_incorrect_type(self, "category_name", str)
        raise_if_missing_or_incorrect_type(self, "category_description", str)
        raise_if_missing_or_incorrect_type(self, "name_field", str)
        raise_if_incorrect_type(self, "fields", list)
        raise_if_incorrect_type(self, "primary_key_field", str)
        raise_if_incorrect_type(self, "description", str)
        raise_if_incorrect_type(self, "created_date_field", str)
        raise_if_incorrect_type(self, "last_modified_date_field", str)
        raise_if_incorrect_type(self, "references", dict)
        raise_if_incorrect_type(self, "owner", tuple)
