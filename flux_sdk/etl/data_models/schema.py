from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union


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
@dataclass
class SchemaField:
    # This maps to the field name in the Rippling Custom Object.
    name: str

    # This is a longer explanation of the field that will appear in the Rippling Custom Object UI.
    description: str

    # This indicates the data type used in the Rippling Custom Object.
    data_type: SchemaDataType

    # When enabled, this value will be required to be not empty by Rippling Custom Object.
    is_required: bool

    # When enabled, this value will be enforced as unique by Rippling Custom Object.
    is_unique: bool

    # When using an Enum data type, this indicates the possible values.
    enum_values: Optional[list[str]]

    # When using an Enum data type, this indicates if *only* enum_values are accepted, meaning anything else will be
    # rejected with an error.
    enum_restricted: bool


# This allows creating a reference to an existing Custom Object.
@dataclass
class CustomObjectReference:
    object: str
    lookup: str


# These are the available lookup-fields for an employee lookup.
class EmployeeLookup(Enum):
    EMPLOYEE_ID = "employee_id"
    BUSINESS_EMAIL = "business_email"
    PERSONAL_EMAIL = "personal_email"


# This allows creating a reference to a Rippling employee.
@dataclass
class EmployeeReference:
    lookup: EmployeeLookup


# This lists the available types that can be used for schema references.
Reference = Union[CustomObjectReference, EmployeeReference]


# A schema describes the shape of an object being imported and is used by Rippling to define the Custom Object.
@dataclass
class Schema:
    # This is the name of the Custom Object.
    name: str

    # This is a more detailed explanation of the field which will appear in the Rippling Custom Object UI.
    description: Optional[str]

    # This is used to put this Custom Object into a group/category. If a category with this name already exists, a new
    # one will not be created.
    category_name: str

    # When creating a new group/category, this will set a description that will appear in the Rippling Custom Object UI.
    # If the category already exists, the description will be updated.
    category_description: Optional[str]

    # This is the name of the field used for the primary key (aka: External ID).
    primary_key_field: str

    # This is the name of the field used for the record name, which is displayed in the Rippling Custom Object UI.
    name_field: str

    # This is the name of the field that reflects when the record was first created.
    created_date_field: str

    # This is the name of the field that reflects when the record was last updated.
    last_modified_date_field: str

    # This is a dedicated reference to a Rippling Employee.
    owner: EmployeeReference

    # These are the links to other objects. The keys are the field names that should be the origin for the link/edge.
    references: dict[str, Reference]

    # These are the remaining data fields.
    fields: list[SchemaField]


