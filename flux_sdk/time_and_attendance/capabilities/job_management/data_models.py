from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Union

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
    """The list of Rippling attributes that are compatible with the attribute, sorted from most compatible to least."""

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "id", str, required=True)
        check_field(self, "name", str, required=True)
        check_field(self, "description", str)
        check_field(self, "compatible_rippling_attribute", list[RipplingAttribute], required=True)

        if len(self.compatible_rippling_attribute) == 0:
            raise ValueError("compatible_rippling_attribute must have at least 1 value")


@dataclass(kw_only=True)
class Address:
    """
    This represents an address.
    """

    street_line_1: str
    """The first line of the street address."""

    street_line_2: Optional[str] = ""
    """The second line of the street address."""

    zip_code: str
    """The zip code of the address."""

    city: str
    """The city of the address."""

    state: str
    """The state of the address."""

    country_code: str
    """The 2 letter uppercase country code of the address."""

    phone: str
    """The phone number of the address."""

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "street_line_1", str, required=True)
        check_field(self, "street_line_2", str)
        check_field(self, "zip_code", str, required=True)
        check_field(self, "city", str, required=True)
        check_field(self, "state", str, required=True)
        check_field(self, "country_code", str, required=True)

        if len(self.country_code) != 2 or self.country_code != self.country_code.upper():
            raise ValueError("country_code must be a 2 letter uppercase country code")

        check_field(self, "phone", str, required=True)

@dataclass(kw_only=True)
class PayRateCompatibleValue:
    """
    This represents a pay rate compatible value.
    """

    job_title: str
    """The job title associated with the pay rate."""

    pay_rate: Optional[float] = None
    """The pay rate associated with the job title."""

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "job_title", str, required=True)

        if self.pay_rate is not None and not isinstance(self.pay_rate, float):
            raise ValueError(f"pay_rate must be a float if provided, got {type(self.pay_rate).__name__} instead.")

@dataclass(kw_only=True)
class JobSiteLocationCompatibleValue:
    """
    This represents a job site location compatible value.
    """

    address: Address
    """The address of the job site location."""

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "address", Address, required=True)

@dataclass(kw_only=True)
class WorkLocationCompatibleValue:
    """
    This represents a work location compatible value.
    """

    name: str
    """The name of the work location."""

    active: bool
    """Whether the work location is enabled or not. This is not the same as whether it is closed for the day."""

    latitude: float
    """The latitude of the work location."""

    longitude: float
    """The longitude of the work location."""

    address: Address
    """The address of the work location."""

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "name", str, required=True)
        check_field(self, "active", bool, required=True)
        check_field(self, "latitude", float, required=True)
        check_field(self, "longitude", float, required=True)
        check_field(self, "address", Address, required=True)

@dataclass(kw_only=True)
class GetJobAttributesValueResponse:
    """
    This represents a response containing the attributes from the third party mapped to their most compatible values.

    For instance, if the third party system has an attribute "work_location" that is most compatible with Rippling's
     "WORK_LOCATION" attribute, and something like the following is defined:

    result = {
        "work_location": [WorkLocationCompatibleValue(name="sf",...), WorkLocationCompatibleValue(...)],
        "pay_rate": [PayRateCompatibleValue(job_title="cashier",...)],
        "job_title": [PayRateCompatibleValue(...)],
    }
    """

    result: Dict[str, List[Union[WorkLocationCompatibleValue, PayRateCompatibleValue, JobSiteLocationCompatibleValue]]]
    """Mapping of attribute name to the list of values that fall under this attribute."""

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "result", dict, required=True)

        if len(self.result) == 0:
            raise ValueError("result must have at least 1 value")

        for key, value in self.result.items():
            if not isinstance(key, str):
                raise ValueError("key must be a string")

            if not isinstance(value, list):
                raise ValueError("value must be a list")

            if len(value) == 0:
                raise ValueError("value must have at least 1 value")

            # make sure values are only of one type per key
            compatible_values = set()
            for val in value:
                if not isinstance(val, (WorkLocationCompatibleValue, PayRateCompatibleValue,
                                        JobSiteLocationCompatibleValue)):
                    raise ValueError("value must be of type .*CompatibleValue")
                compatible_values.add(val)

            if len(compatible_values) != 1:
                raise ValueError("value must be of the same type per key")





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

