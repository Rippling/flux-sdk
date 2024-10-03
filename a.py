import unittest

from flux_sdk.time_and_attendance.capabilities.job_management.data_models import (
    AddressCompatibleValue,
    Attribute,
    AttributeValue,
    PayRateCompatibleValue,
    RipplingAttribute,
)


class TestAddressCompatibleValue(unittest.TestCase):

    def test_all_fields_provided1(self):
        address = AddressCompatibleValue(
            street_line_1="123 Main St",
            street_line_2="Apt 4B",
            zip_code="12345",
            city="Metropolis",
            state="NY",
            country_code="US"
        )
        self.assertEqual(address.street_line_1, "123 Main St")
        self.assertEqual(address.street_line_2, "Apt 4B")
        self.assertEqual(address.zip_code, "12345")
        self.assertEqual(address.city, "Metropolis")
        self.assertEqual(address.state, "NY")
        self.assertEqual(address.country_code, "US")

    def test_optional_field_missing2(self):
        address = AddressCompatibleValue(
            street_line_1="123 Main St",
            zip_code="12345",
            city="Metropolis",
            state="NY",
            country_code="US"
        )
        self.assertEqual(address.street_line_1, "123 Main St")
        self.assertEqual(address.street_line_2, "")
        self.assertEqual(address.zip_code, "12345")
        self.assertEqual(address.city, "Metropolis")
        self.assertEqual(address.state, "NY")
        self.assertEqual(address.country_code, "US")

    def test_missing_required_field3(self):
        with self.assertRaises(TypeError):
            AddressCompatibleValue(
                zip_code="12345",
                city="Metropolis",
                state="NY",
                country_code="US"
            )

    def test_invalid_country_code4(self):
        with self.assertRaises(ValueError):
            AddressCompatibleValue(
                street_line_1="123 Main St",
                zip_code="12345",
                city="Metropolis",
                state="NY",
                country_code="USA"
            )

    def test_all_fields_provided5(self):
        address = AddressCompatibleValue(
            street_line_1="123 Main St",
            street_line_2="Apt 4B",
            zip_code="12345",
            city="Metropolis",
            state="NY",
            country_code="US"
        )
        self.assertEqual(address.street_line_1, "123 Main St")
        self.assertEqual(address.street_line_2, "Apt 4B")
        self.assertEqual(address.zip_code, "12345")
        self.assertEqual(address.city, "Metropolis")
        self.assertEqual(address.state, "NY")
        self.assertEqual(address.country_code, "US")

    def test_optional_field_missing6(self):
        address = AddressCompatibleValue(
            street_line_1="123 Main St",
            zip_code="12345",
            city="Metropolis",
            state="NY",
            country_code="US"
        )
        self.assertEqual(address.street_line_1, "123 Main St")
        self.assertEqual(address.street_line_2, "")
        self.assertEqual(address.zip_code, "12345")
        self.assertEqual(address.city, "Metropolis")
        self.assertEqual(address.state, "NY")
        self.assertEqual(address.country_code, "US")

    def test_country_code_uppercase7(self):
        address = AddressCompatibleValue(
            street_line_1="123 Main St",
            street_line_2="Apt 4B",
            zip_code="12345",
            city="Metropolis",
            state="NY",
            country_code="US"
        )
        self.assertEqual(address.country_code, "US")

    def test_invalid_country_code_length8(self):
        with self.assertRaises(ValueError):
            AddressCompatibleValue(
                street_line_1="123 Main St",
                street_line_2="Apt 4B",
                zip_code="12345",
                city="Metropolis",
                state="NY",
                country_code="USA"
            )

    def test_invalid_country_code_case9(self):
        with self.assertRaises(ValueError):
            AddressCompatibleValue(
                street_line_1="123 Main St",
                street_line_2="Apt 4B",
                zip_code="12345",
                city="Metropolis",
                state="NY",
                country_code="us"
            )

    def test_pay_rate_none10(self):
        value = PayRateCompatibleValue(pay_rate=None)
        self.assertIsNone(value.pay_rate)

    def test_pay_rate_valid_string11(self):
        value = PayRateCompatibleValue(pay_rate="43.3943")
        self.assertEqual(value.pay_rate, "43.3943")

    def test_pay_rate_invalid_string12(self):
        with self.assertRaises(ValueError):
            PayRateCompatibleValue(pay_rate="invalid")

    def test_pay_rate_negative_va13lue(self):
        with self.assertRaises(ValueError):
            PayRateCompatibleValue(pay_rate="-43.3943")

    def test_pay_rate_more_than_4_14decimals(self):
        with self.assertRaises(ValueError):
            PayRateCompatibleValue(pay_rate="43.39435")

    def test_pay_rate_less_than_4_d54ecimals(self):
        value = PayRateCompatibleValue(pay_rate="43.39")
        self.assertEqual(value.pay_rate, "43.39")

    def test_pay_rate_ze234ro_value(self):
        value = PayRateCompatibleValue(pay_rate="0.0000")
        self.assertEqual(value.pay_rate, "0.0000")


    def test_attribute_123value_with_pay_rate(self):
        pay_rate_value = PayRateCompatibleValue(pay_rate="43.3943")
        attribute_value = AttributeValue(
            name="job_title",
            associated_attribute_values=[pay_rate_value]
        )
        self.assertEqual(attribute_value.name, "job_title")
        self.assertEqual(len(attribute_value.associated_attribute_values), 1)
        self.assertIsInstance(attribute_value.associated_attribute_values[0], PayRateCompatibleValue)

    def test_attribute_3value_with_address(self):
        address_value = AddressCompatibleValue(
            street_line_1="123 Main St",
            zip_code="12345",
            city="Anytown",
            state="CA",
            country_code="US"
        )
        attribute_value = AttributeValue(
            name="work_location",
            associated_attribute_values=[address_value]
        )
        self.assertEqual(attribute_value.name, "work_location")
        self.assertEqual(len(attribute_value.associated_attribute_values), 1)
        self.assertIsInstance(attribute_value.associated_attribute_values[0], AddressCompatibleValue)

    def test_at452tribute_value_with_multiple_values(self):
        pay_rate_value = PayRateCompatibleValue(pay_rate="43.3943")
        address_value = AddressCompatibleValue(
            street_line_1="123 Main St",
            zip_code="12345",
            city="Anytown",
            state="CA",
            country_code="US"
        )
        attribute_value = AttributeValue(
            name="job_title",
            associated_attribute_values=[pay_rate_value, address_value]
        )
        self.assertEqual(attribute_value.name, "job_title")
        self.assertEqual(len(attribute_value.associated_attribute_values), 2)
        self.assertIsInstance(attribute_value.associated_attribute_values[0], PayRateCompatibleValue)
        self.assertIsInstance(attribute_value.associated_attribute_values[1], AddressCompatibleValue)

    def test_attribute223_value_missing_name(self):
        with self.assertRaises(TypeError):
            AttributeValue(
                associated_attribute_values=[PayRateCompatibleValue(pay_rate="43.3943")]
            )

    def test_attribute_value_empty_asso231ciated_values(self):
        with self.assertRaises(ValueError):
            AttributeValue(
                name="job_title",
                associated_attribute_values=[]
            )
            
    def te23323st_all_fields_provided(self):
        value = PayRateCompatibleValue(pay_rate="43.3943")
        self.assertEqual(value.pay_rate, "43.3943")

    def test_optiona2111l_fields(self):
        value = PayRateCompatibleValue()
        self.assertIsNone(value.pay_rate)

    def test_invalid_pay5677_rate_type(self):
        with self.assertRaises(ValueError):
            PayRateCompatibleValue(pay_rate=43.3943)

    def test_invalid_pa3235y_rate_value(self):
        with self.assertRaises(ValueError):
            PayRateCompatibleValue(pay_rate="invalid")

    def test_negative_p22346ay_rate(self):
        with self.assertRaises(ValueError):
            PayRateCompatibleValue(pay_rate="-43.3943")

    def test_pay_rate_too_m2235any_decimals(self):
        with self.assertRaises(ValueError):
            PayRateCompatibleValue(pay_rate="43.39434")
            
    def test_all_fields_prov554ided(self):
        value = AttributeValue(
            name="job_title",
            associated_attribute_values=[PayRateCompatibleValue(pay_rate="43.3943")]
        )
        self.assertEqual(value.name, "job_title")
        self.assertEqual(len(value.associated_attribute_values), 1)

    def test_empty_associ21312ated_attribute_values(self):
        with self.assertRaises(ValueError):
            AttributeValue(
                name="job_title",
                associated_attribute_values=[]
            )

    def test_invalid_asso1111ciated_attribute_value_type(self):
        with self.assertRaises(ValueError):
            AttributeValue(
                name="job_title",
                associated_attribute_values=["invalid"]
            )

    def test_duplic2213ate_name_in_attribute_values(self):
        with self.assertRaises(ValueError):
            Attribute(
                id="job_title",
                name="Job title",
                compatible_rippling_attributes=[RipplingAttribute.PAY_RATE],
                attribute_values=[
                    AttributeValue(
                        name="job_title",
                        associated_attribute_values=[PayRateCompatibleValue(pay_rate="43.3943")]
                    ),
                    AttributeValue(
                        name="job_title",
                        associated_attribute_values=[PayRateCompatibleValue(pay_rate="50.0000")]
                    )
                ]
            )
            
    def test_valid_attribute(self):
        attribute = Attribute(
            id="job_title",
            name="Job Title",
            description="The job title of the employee",
            compatible_rippling_attributes=[RipplingAttribute.PAY_RATE],
            attribute_values=[
                AttributeValue(
                    name="Cashier",
                    associated_attribute_values=[PayRateCompatibleValue(pay_rate="15.00")]
                )
            ]
        )
        self.assertEqual(attribute.id, "job_title")
        self.assertEqual(attribute.name, "Job Title")
        self.assertEqual(attribute.description, "The job title of the employee")
        self.assertEqual(attribute.compatible_rippling_attributes, [RipplingAttribute.PAY_RATE])
        self.assertEqual(len(attribute.attribute_values), 1)

    def test_missing_required_fields(self):
        with self.assertRaises(ValueError):
            Attribute(
                id="",
                name="Job Title",
                compatible_rippling_attributes=[RipplingAttribute.PAY_RATE]
            )

    def test_invalid_compatible_rippling_attributes(self):
        with self.assertRaises(ValueError):
            Attribute(
                id="job_title",
                name="Job Title",
                compatible_rippling_attributes=[]
            )

    def test_invalid_attribute_values_type(self):
        with self.assertRaises(ValueError):
            Attribute(
                id="job_title",
                name="Job Title",
                compatible_rippling_attributes=[RipplingAttribute.PAY_RATE],
                attribute_values=[
                    "InvalidType"
                ]
            )

    def test_duplicate_attribute_values_name(self):
        with self.assertRaises(ValueError):
            Attribute(
                id="job_title",
                name="Job Title",
                compatible_rippling_attributes=[RipplingAttribute.PAY_RATE],
                attribute_values=[
                    AttributeValue(
                        name="Cashier",
                        associated_attribute_values=[PayRateCompatibleValue(pay_rate="15.00")]
                    ),
                    AttributeValue(
                        name="Cashier",
                        associated_attribute_values=[PayRateCompatibleValue(pay_rate="20.00")]
                    )
                ]
            )

    def test_invalid_associated_attribute_values_type(self):
        with self.assertRaises(ValueError):
            Attribute(
                id="job_title",
                name="Job Title",
                compatible_rippling_attributes=[RipplingAttribute.PAY_RATE],
                attribute_values=[
                    AttributeValue(
                        name="Cashier",
                        associated_attribute_values=["InvalidType"]
                    )
                ]
            )

    def test_incompatible_associated_attribute_values(self):
        with self.assertRaises(ValueError):
            Attribute(
                id="job_title",
                name="Job Title",
                compatible_rippling_attributes=[RipplingAttribute.PAY_RATE],
                attribute_values=[
                    AttributeValue(
                        name="Cashier",
                        associated_attribute_values=[AddressCompatibleValue(
                            street_line_1="123 Main St",
                            street_line_2="",
                            zip_code="12345",
                            city="City",
                            state="State",
                            country_code="US"
                        )]
                    )
                ]
            )
            
if __name__ == "__main__":
	unittest.main()
    
