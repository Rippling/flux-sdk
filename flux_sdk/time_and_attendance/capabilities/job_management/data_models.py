from dataclasses import dataclass
from typing import Optional
from enum import Enum

from flux_sdk.flux_core.validation import check_field


class RipplingAttribute(Enum):
    """
    This represents the supported attributes in Rippling.
    Your third-party system attributes should be mapped to one or more of these attributes.
    """
    Department = "DEPARTMENT"
    WorkLocation = "WORK_LOCATION"
    PayRate = "PAY_RATE"
    Ein = "EIN"
    JobSiteLocation = "JOB_SITE_LOCATION"

@dataclass(kw_only=True)
class Attributes(kw_only=True):
    """
    This represents an attribute from the third party system and how it is mapped to Rippling.
    """

    id: str
    """The unique id associated with the attribute."""

    name: str
    """The unique name associated with the attribute."""

    description: Optional[str] = ""
    """The optional description associated with the attribute."""

    matching_rippling_attribute: list[RipplingAttribute]
    """The list of Rippling attributes that match the attribute."""

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "id", str, required=True)
        check_field(self, "name", str, required=True)
        check_field(self, "description", str)
        check_field(self, "matching_rippling_attribute", list[RipplingAttribute], required=True)

        if len(self.matching_rippling_attribute) == 0:
            raise ValueError("matching_rippling_attribute must have at least 1 value")

@dataclass(kw_only=True)
class GetJobAttributesResponse:
    """
    This represents a response containing the attributes from the third party system.
    """

    attributes: list[Attributes]
    """The attributes from the third party system and how they map to Rippling."""

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "attributes", list[Attributes], required=True)

        if len(self.attributes) == 0:
            raise ValueError("attributes must have at least 1 value")

