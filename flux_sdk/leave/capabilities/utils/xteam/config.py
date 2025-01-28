from datetime import date
from typing import Optional

class BaseConfig:
    def __init__(
        self,
        customer_count: int,
        file_name: str,
        date_file_created: date,
        customer_name: str,
        file_version_number: str,
        customer_number: int,
        transaction_code: str,
        employee_group_id: Optional[str] = None,
        employee_class_code: Optional[str] = None,
        reporting_level_1: Optional[str] = None,
        key_employee_indicator: Optional[str] = None,
        flight_crew: Optional[str] = None,
        fmla_radius: Optional[str] = None
    ):
        self.customer_count = self.validate_customer_count(customer_count)
        self.file_name = file_name
        self.date_file_created = date_file_created
        self.customer_name = customer_name
        self.file_version_number = file_version_number
        self.customer_number = customer_number
        self.transaction_code = self.validate_transaction_code(transaction_code)
        self.employee_group_id = employee_group_id
        self.employee_class_code = employee_class_code
        self.reporting_level_1 = reporting_level_1
        self.key_employee_indicator = self.validate_indicator(key_employee_indicator, "Key Employee Indicator")
        self.flight_crew = self.validate_indicator(flight_crew, "Flight Crew")
        self.fmla_radius = self.validate_indicator(fmla_radius, "FMLA Radius")

    @staticmethod
    def validate_customer_count(count: int) -> int:
        if count < 1:
            raise ValueError("Customer Count must be at least 1.")
        return count

    @staticmethod
    def validate_transaction_code(code: str) -> str:
        if code not in ["E", "D"]:
            raise ValueError("Transaction Code must be 'E' for Employee or 'D' for Dependent.")
        return code

    @staticmethod
    def validate_indicator(value: Optional[str], field_name: str) -> Optional[str]:
        if value is not None and value not in ["Y", "N"]:
            raise ValueError(f"{field_name} must be 'Y' or 'N'.")
        return value
