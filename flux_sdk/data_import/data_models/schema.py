from dataclasses import dataclass
from enum import StrEnum
from typing import Union


# These are the data types supported by Rippling Custom Objects.
class SchemaDataType(StrEnum):
    Bool = "bool"
    Currency = "currency"
    Date = "date"
    DateTime = "datetime"
    Decimal = "decimal"
    Email = "email"
    Integer = "integer"
    LongText = "longtext"
    Percent = "percent"
    String = "string"
    Time = "time"
    Url = "url"


# A field usually corresponds to a column in a database, it is one datum within a Record.
@dataclass
class SchemaField:
    # This maps to the field name in the Rippling Custom Object.
    name: str

    # This is a longer description of the field that will appear in the Rippling Custom Object UI.
    description: str

    # This indicates the data type used in the Rippling Custom Object.
    data_type: SchemaDataType

    # When enabled, this value will be required to be not empty by Rippling Custom Object.
    is_required: bool

    # When enabled, this value will be enforced as unique by Rippling Custom Object.
    is_unique: bool


# These are the available lookup-fields for an employee lookup.
class EmployeeLookup(StrEnum):
    EMPLOYEE_ID = "employee_id"
    BUSINESS_EMAIL = "work_email"
    PERSONAL_EMAIL = "personal_email"


# This is a helper for creating a link/reference to a Rippling employee.
@dataclass
class EmployeeReference:
    lookup: EmployeeLookup


@dataclass
class CustomObjectReference:
    object: str
    lookup: str


# This lists the available types that can be used for schema references.
ReferenceType = Union[CustomObjectReference, EmployeeReference]


# A schema describes the shape of an object being imported and is used by Rippling to define the Custom Object.
@dataclass
class Schema:
    # This is the name of the Custom Object.
    name: str

    # This indicates which field (by name) is used as the ID for the object.
    primary_key: str

    # These are the links to other objects. The keys are the field names that should be the origin for the link/edge.
    references: dict[str, ReferenceType]

    # These are the remaining data fields.
    fields: list[SchemaField]


