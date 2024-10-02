from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Optional, Union

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
class PayRateCompatibleValue:
    """
    This represents a pay rate compatible value.
    """

    pay_rate: Optional[str] = None
    """The pay rate associated with the job title, str with max 4 decimals, for ex, 43.3943"""

    def __post_init__(self):
        """Perform validation."""
        if self.pay_rate is not None:
            if self.pay_rate and not isinstance(self.pay_rate, str):
                raise ValueError("PayRateCompatibleValue error: pay_rate must be a str.")

            try:
                decimal = Decimal(self.pay_rate)
            except Exception:
                raise ValueError("PayRateCompatibleValue error: pay_rate must be a valid number")

            if decimal < 0:
                raise ValueError("PayRateCompatibleValue error: pay_rate must be a positive number")
            if decimal.as_tuple().exponent < -4:
                raise ValueError("PayRateCompatibleValue error: pay_rate must have at most 4 decimal places")


@dataclass(kw_only=True)
class AddressCompatibleValue:
    """
    This represents an address compatible value.
    """

    street_line_1: str
    """The first line of the street address. """

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

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "street_line_1", str, required=True)
        check_field(self, "street_line_2", str)
        check_field(self, "zip_code", str, required=True)
        check_field(self, "city", str, required=True)
        check_field(self, "state", str, required=True)
        check_field(self, "country_code", str, required=True)

        if len(self.country_code) != 2 or self.country_code != self.country_code.upper():
            raise ValueError("AddressCompatibleValue error: country_code must be a 2 letter uppercase country code")


@dataclass(kw_only=True)
class AttributeValue:
    """
    This represents an attribute value associated with an attribute.

    Each attribute value will have a name, and a list of associated attribute values based on the
    compatible_rippling_attributes field.
    """

    name: str
    """
    The unique value associated with the attribute. Please strip any whitespaces.
    For ex, if the attribute was "job_title", the value could be "Cashier".
    """

    associated_attribute_values: list[Union[PayRateCompatibleValue, AddressCompatibleValue]]
    """
    The non-empty list of associated attribute values based on compatible_rippling_attributes.
    For ex, if the attribute was "job_title" and compatible_rippling_attributes was [PAY_RATE], 
    the associated_attribute_values should be [PayRateCompatibleValue(...)].
    
    If the compatible_rippling_attributes was [WORK_LOCATION] or [JOB_SITE_LOCATION] (or both), 
    the associated_attribute_values could be [AddressCompatibleValue(...)].
    """

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "name", str, required=True)
        check_field(self, "associated_attribute_values", list, required=True)

        if len(self.associated_attribute_values) == 0:
            raise ValueError("AttributeValue error: associated_attribute_values must have at least 1 value")

        for value in self.associated_attribute_values:
            if not isinstance(value, (PayRateCompatibleValue, AddressCompatibleValue)):
                raise ValueError(
                    "AttributeValue error: associated_attribute_values must be of type PayRateCompatibleValue or "
                    "AddressCompatibleValue"
                )


@dataclass(kw_only=True)
class Attribute:
    """
    This represents an attribute from the third party system and how it is mapped to Rippling.

    Attribute values should also be provided if requested by Rippling.
    """

    id: str
    """The unique id associated with the attribute, for ex, job_title."""

    name: str
    """The unique name associated with the attribute, for ex, "Job title". Please strip any whitespaces."""

    description: Optional[str] = ""
    """The optional description associated with the attribute."""

    compatible_rippling_attributes: list[RipplingAttribute]
    """
    The non-empty list of Rippling attributes that are compatible with the attribute, 
    sorted from most compatible to least, for ex, [PAY_RATE].
    """

    attribute_values: Optional[list[AttributeValue]] = None
    """
    The non-empty (if not None) list of attribute values associated with the attribute.
    This field should only be used if requested_attribute_values is True in GetJobAttributesRequest.
    Note that attribute name should be unique across attribute_values.
    """

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "id", str, required=True)
        check_field(self, "name", str, required=True)
        check_field(self, "description", str)
        check_field(self, "compatible_rippling_attributes", list, required=True)

        rippling_attributes_to_attribute_values = {
            RipplingAttribute.PAY_RATE: PayRateCompatibleValue,
            RipplingAttribute.JOB_SITE_LOCATION: AddressCompatibleValue,
            RipplingAttribute.WORK_LOCATION: AddressCompatibleValue
        }
        allowed_compatible_values = [rippling_attributes_to_attribute_values[attribute]
                                     for attribute in self.compatible_rippling_attributes]

        if len(self.compatible_rippling_attributes) == 0:
            raise ValueError("Attribute error: compatible_rippling_attributes must have at least 1 value")

        for attribute in self.compatible_rippling_attributes:
            if not isinstance(attribute, RipplingAttribute):
                raise ValueError("Attribute error: compatible_rippling_attributes must be of type RipplingAttribute")

        if self.attribute_values is not None:
            if len(self.attribute_values) == 0:
                raise ValueError("Attribute error: attribute_values must have at least 1 value")

            names = set()
            associated_attribute_values_types = set()
            for value in self.attribute_values:
                if not isinstance(value, AttributeValue):
                    raise ValueError("Attribute error: attribute_values must be of type AttributeValue")
                for associated_attribute_values in value.associated_attribute_values:
                    associated_attribute_values_types.add(type(associated_attribute_values))
                if value.name.strip().lower() in names:
                    raise ValueError(f"Attribute error: duplicate name in attribute_values: {value.name}")
                names.add(value.name.strip().lower())

            if associated_attribute_values_types != set(allowed_compatible_values):
                raise ValueError(
                    f"Attribute error: associated_attribute_values in attribute_values must be of type"
                    f" {allowed_compatible_values}"
                )



@dataclass(kw_only=True)
class GetJobAttributesRequest:
    """
    This represents a request to fetch the attributes from the third party system, how they map to Rippling,
    and optionally their values.

    If we require the values of the attributes, requested_attribute_values will be True.

    We may also only request information about certain attributes through requested_attributes.
    """

    requested_attribute_values: bool
    """
    Whether to fetch the values of the attributes or not.
    If False, GetJobAttributesResponse will only contain the list of attributes and how they map to Rippling.
    If True, GetJobAttributesResponse will also contain the values of the attributes in addition to their mappings.
    """

    requested_attributes: list[str] | None = None
    """
    The third party attributes to fetch the values for. If None, all attributes should be fetched.
    Note, it is recommended to use the key_in_requested_attributes helper.
    """

    def key_in_requested_attributes(self, key: str) -> bool:
        """
        Check if the key is in the requested attributes.
        Returns True if key exists, or if requested_attributes is None.
        """
        return self.requested_attributes is None or key in self.requested_attributes

    def __post_init__(self):
        """Perform validation."""
        if self.requested_attribute_values not in [False, True]:
            raise ValueError("GetJobAttributesRequest error: requested_attribute_values must be a bool")

        if self.requested_attributes is not None:
            if not isinstance(self.requested_attributes, list):
                raise ValueError("GetJobAttributesRequest error: requested_attributes must be a list if provided")
            if len(self.requested_attributes) == 0:
                raise ValueError("GetJobAttributesRequest error: requested_attributes must have at least 1 value")


@dataclass(kw_only=True)
class GetJobAttributesResponse:
    """
    This represents a response containing the attributes from the third party system, how they map to Rippling,
    and optionally their values.

    See GetJobAttributesRequest to determine if values are requested, and which attributes are requested.
    """

    attributes: list[Attribute]
    """
    The non-empty list of attributes from the third party system and how they map to Rippling.
    The value of the attributes may also be requested.
    """

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "attributes", list[Attribute], required=True)

        if len(self.attributes) == 0:
            raise ValueError("GetJobAttributesResponse error: attributes must have at least 1 value")

        ids = set()
        names = set()
        for attribute in self.attributes:
            if attribute.id in ids:
                raise ValueError(f"GetJobAttributesResponse error: duplicate id in attributes: {attribute.id}")
            if attribute.name.strip().lower() in names:
                raise ValueError(f"GetJobAttributesResponse error: duplicate name in attributes: {attribute.name}")
            ids.add(attribute.id)
            names.add(attribute.name.strip().lower())
