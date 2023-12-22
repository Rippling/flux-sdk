from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from flux_sdk.flux_core.validation import check_field


class SchemaDataType(Enum):
    """These are the data types supported by Rippling Custom Objects."""
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


@dataclass(kw_only=True)
class SchemaField:
    """A field usually corresponds to a column in a database, it is one datum within a Record."""

    name: str
    """This maps to the field name in the Rippling Custom Object."""

    data_type: SchemaDataType
    """This indicates the data type used in the Rippling Custom Object."""

    description: Optional[str] = None
    """This is a longer explanation of the field that will appear in the Rippling Custom Object UI."""

    is_required: bool = False
    """When enabled, this value will be required to be not empty by Rippling Custom Object."""

    is_unique: bool = False
    """When enabled, this value will be enforced as unique by Rippling Custom Object."""

    enum_values: Optional[list[str]] = None
    """When using an Enum data type, this indicates the possible values."""

    enum_restricted: bool = False
    """
    When using an Enum data type, this indicates if *only* enum_values are accepted, meaning anything else will be
    rejected with an error.
    """

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "name", str, required=True)
        check_field(self, "data_type", SchemaDataType, required=True)
        check_field(self, "description", str)
        check_field(self, "enum_values", list)
        check_field(self, "is_required", bool)
        check_field(self, "is_unique", bool)
        check_field(self, "enum_restricted", bool)

        if self.data_type in [SchemaDataType.Enum, SchemaDataType.MultiEnum]:
            if len(self.enum_values) == 0:
                raise ValueError("enum_values must have at least 1 value")


@dataclass(kw_only=True)
class CustomObjectReference:
    """This allows creating a reference to an existing Custom Object."""

    object: str
    """The name of the Custom Object to link to."""

    lookup: str
    """The name of the field on the Custom Object to use for the link."""

    description: Optional[str] = None
    """An optional explanation for this reference to be shown in the Rippling Custom Object UI."""

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "object", str, required=True)
        check_field(self, "lookup", str, required=True)
        check_field(self, "description", str)


class EmployeeLookup(Enum):
    """These are the available lookup-fields for a Rippling Employee."""

    EMPLOYEE_ID = "employee_id"
    """The Rippling Employee ID."""

    PERSONAL_EMAIL = "personal_email"
    """The personal email for a Rippling Employee."""

    WORK_EMAIL = "work_email"
    """The work/business email for a Rippling Employee."""


@dataclass(kw_only=True)
class EmployeeReference:
    """This allows creating a reference to a Rippling employee."""

    lookup: EmployeeLookup
    """The name of the field on the Employee object to use for the link."""

    description: Optional[str] = None
    """An optional explanation for this reference to be shown in the Rippling Custom Object UI."""

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "lookup", EmployeeLookup, required=True)
        check_field(self, "description", str)


Reference = Union[CustomObjectReference, EmployeeReference]
"""This lists the available types that can be used for schema references."""


@dataclass(kw_only=True)
class Schema:
    """A schema describes the shape of an object being imported and is used by Rippling to define the Custom Object."""

    name: str
    """This is the name of the Custom Object."""

    category_name: str
    """
    This is used to put this Custom Object into a group/category. If a category with this name already exists, a new one
    will not be created. If this value is changed, no categories will be deleted as they could be used by another
    object.
    """

    category_description: str
    """
    When creating a new group/category, this will set a description that will appear in the Rippling Custom Object UI.
    If the category already exists, the description will be updated.
    """

    primary_key_field: str
    """This is the name of the field used for the primary key (aka: External ID)."""

    name_field: str
    """This is the name of the field used for the record name, which is displayed in the Rippling Custom Object UI."""

    fields: list[SchemaField]
    """These are the remaining data fields."""

    description: Optional[str] = None
    """This is a more detailed explanation of the field which will appear in the Rippling Custom Object UI."""

    created_date_field: Optional[str] = None
    """
    This is the name of the field that reflects when the record was first created. When a field name is not provided,
    Rippling will use the time that the record is first imported.
    """

    last_modified_date_field: Optional[str] = None
    """
    This is the name of the field that reflects when the record was last updated. When a field name is not provided,
    Rippling will use the time that the record was last updated.
    """

    references: Optional[dict[str, Reference]] = None
    """
    These are the links to other objects. The keys are the field names that should be the origin for the link/edge.
    """

    owner: Optional[tuple[str, EmployeeReference]] = None
    """This establishes the built-in link to Employee, if applicable."""

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "name", str, required=True)
        check_field(self, "category_name", str, required=True)
        check_field(self, "category_description", str, required=True)
        check_field(self, "primary_key_field", str, required=True)
        check_field(self, "name_field", str, required=True)
        check_field(self, "fields", list[SchemaField])
        check_field(self, "description", str)
        check_field(self, "created_date_field", str)
        check_field(self, "last_modified_date_field", str)
        check_field(self, "references", dict[str, Reference])
        check_field(self, "owner", tuple[str, EmployeeReference])
