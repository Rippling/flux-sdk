import unittest
from decimal import Decimal
from flux_sdk.time_and_attendance.capabilities.job_management.data_models import (
    Attribute, Address, PayRateCompatibleValue, JobSiteLocationCompatibleValue, WorkLocationCompatibleValue, GetJobAttributeValuesResponse, GetJobAttributesResponse, RipplingAttribute
)

class TestDataModels(unittest.TestCase):

    def test_attribute_post_init(self):
        attr = Attribute(
            id="1",
            name="Test Attribute",
            description="A test attribute",
            compatible_rippling_attribute=[RipplingAttribute.DEPARTMENT]
        )
        self.assertEqual(attr.id, "1")
        self.assertEqual(attr.name, "Test Attribute")
        self.assertEqual(attr.description, "A test attribute")
        self.assertEqual(attr.compatible_rippling_attribute, [RipplingAttribute.DEPARTMENT])

    def test_address_post_init(self):
        address = Address(
            street_line_1="123 Main St",
            street_line_2="Apt 4",
            zip_code="12345",
            city="Test City",
            state="TS",
            country_code="US"
        )
        self.assertEqual(address.street_line_1, "123 Main St")
        self.assertEqual(address.street_line_2, "Apt 4")
        self.assertEqual(address.zip_code, "12345")
        self.assertEqual(address.city, "Test City")
        self.assertEqual(address.state, "TS")
        self.assertEqual(address.country_code, "US")

    def test_pay_rate_compatible_value_post_init(self):
        value = PayRateCompatibleValue(
            name="Cashier",
            pay_rate="43.3943"
        )
        self.assertEqual(value.name, "Cashier")
        self.assertEqual(value.pay_rate, "43.3943")

    def test_job_site_location_compatible_value_post_init(self):
        address = Address(
            street_line_1="123 Main St",
            street_line_2="Apt 4",
            zip_code="12345",
            city="Test City",
            state="TS",
            country_code="US"
        )
        value = JobSiteLocationCompatibleValue(
            name="San Francisco",
            address=address
        )
        self.assertEqual(value.name, "San Francisco")
        self.assertEqual(value.address, address)

    def test_work_location_compatible_value_post_init(self):
        address = Address(
            street_line_1="123 Main St",
            street_line_2="Apt 4",
            zip_code="12345",
            city="Test City",
            state="TS",
            country_code="US"
        )
        value = WorkLocationCompatibleValue(
            name="San Francisco",
            address=address
        )
        self.assertEqual(value.name, "San Francisco")
        self.assertEqual(value.address, address)

    def test_get_job_attribute_values_response_post_init(self):
        address = Address(
            street_line_1="123 Main St",
            street_line_2="Apt 4",
            zip_code="12345",
            city="Test City",
            state="TS",
            country_code="US"
        )
        value = WorkLocationCompatibleValue(
            name="San Francisco",
            address=address
        )
        response = GetJobAttributeValuesResponse(
            result={"location": [value]}
        )
        self.assertEqual(response.result, {"location": [value]})

    def test_get_job_attributes_response_post_init(self):
        attr = Attribute(
            id="1",
            name="Test Attribute",
            description="A test attribute",
            compatible_rippling_attribute=[RipplingAttribute.DEPARTMENT]
        )
        response = GetJobAttributesResponse(
            attributes=[attr]
        )
        self.assertEqual(response.attributes, [attr])

    def test_get_job_attribute_values_response_validation(self):
        with self.assertRaises(ValueError):
            GetJobAttributeValuesResponse(result={})

        with self.assertRaises(ValueError):
            GetJobAttributeValuesResponse(result={"location": []})

        with self.assertRaises(ValueError):
            GetJobAttributeValuesResponse(result={"location": ["invalid"]})

        with self.assertRaises(ValueError):
            GetJobAttributeValuesResponse(result={"location": [WorkLocationCompatibleValue(name="sf", address=None)]})

    def test_get_job_attributes_response_validation(self):
        with self.assertRaises(ValueError):
            GetJobAttributesResponse(attributes=[])

        attr1 = Attribute(
            id="1",
            name="Test Attribute 1",
            description="A test attribute",
            compatible_rippling_attribute=[RipplingAttribute.DEPARTMENT]
        )
        attr2 = Attribute(
            id="1",
            name="Test Attribute 2",
            description="A test attribute",
            compatible_rippling_attribute=[RipplingAttribute.DEPARTMENT]
        )
        with self.assertRaises(ValueError):
            GetJobAttributesResponse(attributes=[attr1, attr2])

        attr3 = Attribute(
            id="2",
            name="Test Attribute 1",
            description="A test attribute",
            compatible_rippling_attribute=[RipplingAttribute.DEPARTMENT]
        )
        with self.assertRaises(ValueError):
            GetJobAttributesResponse(attributes=[attr1, attr3])


if __name__ == "__main__":
    unittest.main()
