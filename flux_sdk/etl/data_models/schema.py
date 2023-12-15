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
        if not self.name:
            raise ValueError("name is required")
        elif type(self.name) is not str:
            raise TypeError("name must be a string")

        if not self.data_type:
            raise ValueError("data_type is required")
        elif not isinstance(self.data_type, SchemaDataType):
            raise TypeError("data_type must be a SchemaDataType")

        if self.description:
            if type(self.description) is not str:
                raise TypeError("description must be a string")

        if type(self.is_required) is not bool:
            raise TypeError("is_required must be a bool")

        if type(self.is_unique) is not bool:
            raise TypeError("is_unique must be a bool")

        if self.enum_values:
            if type(self.enum_values) is not list:
                raise TypeError("enum_values must be a list")

        if type(self.enum_restricted) is not bool:
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
        if not self.object:
            raise ValueError("object is required")
        elif type(self.object) is not str:
            raise TypeError("object must be a string")

        if not self.lookup:
            raise ValueError("lookup is required")
        elif type(self.lookup) is not str:
            raise TypeError("lookup must be a string")

        if self.description:
            if type(self.description) is not str:
                raise TypeError("description must be a string")


# These are the available lookup-fields for a Rippling Employee.
class EmployeeLookup(Enum):
    # The Rippling Employee ID.
    EMPLOYEE_ID = "employee_id"

    # The work/business email for a Rippling Employee.
    BUSINESS_EMAIL = "business_email"

    # The personal email for a Rippling Employee.
    PERSONAL_EMAIL = "personal_email"


# This allows creating a reference to a Rippling employee.
@dataclass(kw_only=True)
class EmployeeReference:
    # The name of the field on the Employee object to use for the link.
    lookup: EmployeeLookup

    # An optional explanation for this reference to be shown in the Rippling Custom Object UI.
    description: Optional[str] = None

    # Perform validation.
    def __post_init__(self):
        if not self.lookup:
            raise ValueError("lookup is required")
        elif not isinstance(self.lookup, EmployeeLookup):
            raise TypeError("lookup must be a EmployeeLookup")

        if self.description:
            if type(self.description) is not str:
                raise TypeError("description must be a string")


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

    # This is the name of the field used for the primary key (aka: External ID).
    primary_key_field: str

    # This is the name of the field used for the record name, which is displayed in the Rippling Custom Object UI. When
    # not provided,
    name_field: str

    # These are the remaining data fields.
    fields: list[SchemaField]

    # This is a more detailed explanation of the field which will appear in the Rippling Custom Object UI.
    description: Optional[str] = None

    # When creating a new group/category, this will set a description that will appear in the Rippling Custom Object UI.
    # If the category already exists, the description will be updated.
    category_description: Optional[str] = None

    # This is the name of the field that reflects when the record was first created. When a field name is not provided,
    # Rippling will use the time that the record is first imported.
    created_date_field: Optional[str] = None

    # This is the name of the field that reflects when the record was last updated. When a field name is not provided,
    # Rippling will use the time that the record was last updated.
    last_modified_date_field: Optional[str] = None

    # These are the links to other objects. The keys are the field names that should be the origin for the link/edge.
    references: Optional[dict[str, Reference]] = None

    # Perform validation.
    def __post_init__(self):
        if not self.name:
            raise ValueError("name is required")
        elif type(self.name) is not str:
            raise TypeError("name must be a string")

        if not self.category_name:
            raise ValueError("category_name is required")
        elif type(self.category_name) is not str:
            raise TypeError("category_name must be a str")

        if not self.primary_key_field:
            raise ValueError("primary_key_field is required")
        elif type(self.primary_key_field) is not str:
            raise TypeError("primary_key_field must be a str")

        if not self.name_field:
            raise ValueError("name_field is required")
        elif type(self.name_field) is not str:
            raise TypeError("name_field must be a str")

        if self.fields:
            if type(self.fields) is not list:
                raise TypeError("fields must be a list")

        if self.description:
            if type(self.description) is not str:
                raise TypeError("description must be a str")

        if self.category_description:
            if type(self.category_description) is not str:
                raise TypeError("category_description must be a str")

        if self.created_date_field:
            if type(self.created_date_field) is not str:
                raise TypeError("created_date_field must be a str")

        if self.last_modified_date_field:
            if type(self.last_modified_date_field) is not str:
                raise TypeError("last_modified_date_field must be a str")

        if self.references:
            if type(self.references) is not dict:
                raise TypeError("references must be a dict")
