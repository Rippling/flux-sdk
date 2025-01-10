from enum import Enum
from typing import Optional
from datetime import date
import re

class EmployeeStatus(Enum):
    ACTIVE = "A"
    LEAVE_OF_ABSENCE = "L"
    TERMINATED = "T"
    RETIRED = "R"
    DECEASED = "D"

class EmploymentType(Enum):
    FULL_TIME = "F"
    PART_TIME = "P"

class ExemptStatus(Enum):
    EXEMPT = "E"
    NON_EXEMPT = "N"

class SalaryBasis(Enum):
    ANNUAL = "A"

class HRIS:
    def __init__(
        self,
        employee_ssn: str,
        employee_id: str,
        employee_home_phone: Optional[str] = None,
        employee_cell_phone: Optional[str] = None,
        employee_personal_email: Optional[str] = None,
        employee_work_email: Optional[str] = None,
        employee_work_state_code: Optional[str] = None,
        employee_work_country_code: Optional[int] = 840,
        employee_work_phone: Optional[str] = None,
        supervisor_id: Optional[str] = None,
        employee_status: Optional[EmployeeStatus] = None,
        employee_status_effective_date: Optional[date] = None,
        employee_service_date: Optional[date] = None,
        rehire_date: Optional[date] = None,
        original_hire_date: Optional[date] = None,
        employment_type: Optional[EmploymentType] = None,
        exempt_status: Optional[ExemptStatus] = None,
        benefit_salary_amount: Optional[float] = None,
        salary_basis: Optional[SalaryBasis] = None,
        salary_effective_date: Optional[date] = None,
        job_title: Optional[str] = None,
        client_field_2: Optional[bool] = None,
        client_field_3: Optional[bool] = None
    ):
        self.employee_ssn = self.validate_ssn(employee_ssn)
        self.employee_id = self.validate_no_hyphens(employee_id, "Employee ID")
        self.employee_home_phone = self.validate_phone(employee_home_phone, "Home Phone")
        self.employee_cell_phone = self.validate_phone(employee_cell_phone, "Cell Phone")
        self.employee_personal_email = self.validate_email(employee_personal_email)
        self.employee_work_email = self.validate_email(employee_work_email)
        self.employee_work_state_code = employee_work_state_code
        self.employee_work_country_code = employee_work_country_code
        self.employee_work_phone = self.validate_phone(employee_work_phone, "Work Phone")
        self.supervisor_id = supervisor_id
        self.employee_status = employee_status
        self.employee_status_effective_date = employee_status_effective_date
        self.employee_service_date = employee_service_date
        self.rehire_date = rehire_date
        self.original_hire_date = original_hire_date
        self.employment_type = employment_type
        self.exempt_status = exempt_status
        self.benefit_salary_amount = benefit_salary_amount
        self.salary_basis = salary_basis
        self.salary_effective_date = salary_effective_date
        self.job_title = job_title
        self.client_field_2 = client_field_2
        self.client_field_3 = client_field_3

    @staticmethod
    def validate_ssn(ssn: str) -> str:
        if not ssn.isdigit():
            raise ValueError("SSN must only contain digits and no hyphens.")
        return ssn

    @staticmethod
    def validate_no_hyphens(value: str, field_name: str) -> str:
        if "-" in value:
            raise ValueError(f"{field_name} must not contain hyphens.")
        return value

    @staticmethod
    def validate_phone(phone: Optional[str], field_name: str) -> Optional[str]:
        if phone and (not phone.isdigit() or len(phone) != 10):
            raise ValueError(f"{field_name} must be a 10-digit number without hyphens.")
        return phone

    @staticmethod
    def validate_email(email: Optional[str]) -> Optional[str]:
        if email:
            email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
            if not re.match(email_regex, email):
                raise ValueError("Invalid email address format.")
        return email
