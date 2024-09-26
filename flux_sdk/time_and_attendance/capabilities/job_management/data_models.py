from dataclasses import dataclass
from enum import Enum
from typing import Optional

from flux_sdk.flux_core.validation import check_field


class RipplingAttribute(Enum):
    """
    This represents the supported attributes in Rippling.
    Your third-party system attributes should be mapped to one or more of these attributes.
    """
    DEPARTMENT = "DEPARTMENT"
    WORK_LOCATION = "WORK_LOCATION"
    PAY_RATE = "PAY_RATE"
    EIN = "EIN"
    JOB_SITE_LOCATION = "JOB_SITE_LOCATION"

@dataclass(kw_only=True)
class Attribute:
    """
    This represents an attribute from the third party system and how it is mapped to Rippling.
    """

    id: str
    """The unique id associated with the attribute."""

    name: str
    """The unique name associated with the attribute."""

    description: Optional[str] = ""
    """The optional description associated with the attribute."""

    compatible_rippling_attribute: list[RipplingAttribute]
    """The list of Rippling attributes that match the attribute."""

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "id", str, required=True)
        check_field(self, "name", str, required=True)
        check_field(self, "description", str)
        check_field(self, "compatible_rippling_attribute", list[RipplingAttribute], required=True)

        if len(self.compatible_rippling_attribute) == 0:
            raise ValueError("compatible_rippling_attribute must have at least 1 value")

@dataclass(kw_only=True)
class GetJobAttributesResponse:
    """
    This represents a response containing the attributes from the third party system.
    """

    attributes: list[Attribute]
    """The attributes from the third party system and how they map to Rippling."""

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "attributes", list[Attribute], required=True)

        if len(self.attributes) == 0:
            raise ValueError("attributes must have at least 1 value")

        ids = set()
        names = set()
        for attribute in self.attributes:
            if attribute.id in ids:
                raise ValueError(f"Duplicate id found: {attribute.id}")
            if attribute.name in names:
                raise ValueError(f"Duplicate name found: {attribute.name}")
            ids.add(attribute.id)
            names.add(attribute.name)

