import unittest

from flux_sdk.time_and_attendance.capabilities.job_management.data_models import (
    EmployeePayRateOverride,
    GetEmployeesPayRateOverridesResponse,
)


class TestGetEmployeesPayRateOverridesResponse(unittest.TestCase):

    
    def test_valid_response(self):
        overrides = {
            "job_title": [
                EmployeePayRateOverride(
                    employee_id="123",
                    attribute_value_name="Cashier",
                    attribute_value_id="123",
                    pay_rate="43.3943"
                )
            ]
        }
        response = GetEmployeesPayRateOverridesResponse(employee_pay_rate_overrides=overrides)
        self.assertEqual(len(response.employee_pay_rate_overrides), 1)

    def test_invalid_attribute_id_type(self):
        overrides = {
            123: [
                EmployeePayRateOverride(
                    employee_id="123",
                    attribute_value_name="Cashier",
                    attribute_value_id="123",
                    pay_rate="43.3943"
                )
            ]
        }
        with self.assertRaises(ValueError):
            GetEmployeesPayRateOverridesResponse(employee_pay_rate_overrides=overrides)

    def test_invalid_pay_rate_override_type(self):
        overrides = {
            "job_title": [
                {
                    "employee_id": "123",
                    "attribute_value_name": "Cashier",
                    "attribute_value_id": "123",
                    "pay_rate": "43.3943"
                }
            ]
        }
        with self.assertRaises(ValueError):
            GetEmployeesPayRateOverridesResponse(employee_pay_rate_overrides=overrides)

    def test_duplicate_attribute_value_id(self):
        overrides = {
            "job_title": [
                EmployeePayRateOverride(
                    employee_id="123",
                    attribute_value_name="Cashier",
                    attribute_value_id="123",
                    pay_rate="43.3943"
                ),
                EmployeePayRateOverride(
                    employee_id="123",
                    attribute_value_name="Cashier",
                    attribute_value_id="123",
                    pay_rate="50.0000"
                )
            ]
        }
        with self.assertRaises(ValueError):
            GetEmployeesPayRateOverridesResponse(employee_pay_rate_overrides=overrides)

    
    def test_multiple_attribute_value_names(self):
        overrides = {
            "job_title": [
                EmployeePayRateOverride(
                    employee_id="123",
                    attribute_value_name="Cashier",
                    attribute_value_id="123",
                    pay_rate="43.3943"
                ),
                EmployeePayRateOverride(
                    employee_id="142",
                    attribute_value_name="asd",
                    attribute_value_id="123",
                    pay_rate="50.0000"
                )
            ]
        }
        with self.assertRaises(ValueError) as x:
            GetEmployeesPayRateOverridesResponse(employee_pay_rate_overrides=overrides)
        print(x.exception)

if __name__ == '__main__':
    unittest.main()