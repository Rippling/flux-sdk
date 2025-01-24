

from flux_sdk.flux_core.data_models import (
    Employee,
    LeaveInfo,
    MonetaryValue,
)

from typing import Optional
from datetime import datetime


class Employee:
    """
    This contains all the details about the employee including personal and job details. Developers are expected to
    use to fill employee details inside the file. If an employee attribute your app requires is
    not present, please reach out to apps@rippling.com to add support for that attribute.
    """
    def __init__(self, 
                 ssn: str,
                 role_id: str,
                 first_name: str,
                 middle_name: str,
                 last_name: str,
                 employee_id: Optional[str],
                 employee_number: Optional[int],
                 job_title: Optional[str],
                 start_date: datetime,
                 original_hire_date: datetime,
                 business_email: str,
                 personal_email: str,
                 gender: str,
                 termination_date: Optional[datetime],
                 w2_start_date: datetime,
                 address: Optional['Address'],
                 status: 'EmployeeState',
                 dob: datetime,
                 phone_number: str,
                 phone_number_v2: Optional['PhoneNumber'],
                 is_temporary: bool,
                 is_hourly: bool,
                 is_salaried: bool,
                 is_contractor: bool,
                 is_full_time: bool,
                 is_part_time: bool,
                 is_new_hire: bool,
                 is_rehire: bool,
                 is_international_employee: bool,
                 marital_status: Optional[str],
                 employment_type: Optional[str],
                 department: Optional[str],
                 termination_reason: Optional[str],
                 work_location_nickname: Optional[str],
                 teams: Optional[list[str]]):
        self.ssn = ssn
        self.role_id = role_id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.employee_id = employee_id
        self.employee_number = employee_number
        self.job_title = job_title
        self.start_date = start_date
        self.original_hire_date = original_hire_date
        self.business_email = business_email
        self.personal_email = personal_email
        self.gender = gender
        self.termination_date = termination_date
        self.w2_start_date = w2_start_date
        self.address = address
        self.status = status
        self.dob = dob
        self.phone_number = phone_number
        self.phone_number_v2 = phone_number_v2
        self.is_temporary = is_temporary
        self.is_hourly = is_hourly
        self.is_salaried = is_salaried
        self.is_contractor = is_contractor
        self.is_full_time = is_full_time
        self.is_part_time = is_part_time
        self.is_new_hire = is_new_hire
        self.is_rehire = is_rehire
        self.is_international_employee = is_international_employee
        self.marital_status = marital_status
        self.employment_type = employment_type
        self.department = department
        self.termination_reason = termination_reason
        self.work_location_nickname = work_location_nickname
        self.teams = teams


class CustomerEmployeeRecord:
    """
    Represents the employee record in the customer-specific format.
    """
    def __init__(self, employee: Employee):
        def format_phone(phone: Optional[str]) -> Optional[str]:
            """Removes non-numeric characters from a phone number."""
            if phone:
                return ''.join(filter(str.isdigit, phone))
            return None

        def validate_email(email: str) -> bool:
            """Validates an email based on customer-specific rules."""
            import re
            pattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
            return bool(re.match(pattern, email))

        self.employee_ssn = employee.ssn.replace("-", "") if employee.ssn else "000000000"
        self.employee_id = employee.employee_id.replace("-", "") if employee.employee_id else "UNKNOWN"
        self.employee_home_phone = format_phone(employee.phone_number_v2.home_phone if hasattr(employee.phone_number_v2, 'home_phone') else None)
        self.employee_cell_phone = format_phone(employee.phone_number_v2.cell_phone if hasattr(employee.phone_number_v2, 'cell_phone') else None)
        self.employee_personal_email = employee.personal_email if validate_email(employee.personal_email) else "unknown@example.com"
        self.employee_work_email = employee.business_email if validate_email(employee.business_email) else "unknown@example.com"
        self.employee_work_state_code = employee.address.state if employee.address else "XX"
        self.employee_work_address_country_code = "840"  # Default to USA
        self.employee_work_phone = format_phone(employee.phone_number_v2.work_phone if hasattr(employee.phone_number_v2, 'work_phone') else None)
        self.supervisor_id = "DEFAULT_SUPERVISOR"  # Default supervisor ID
        self.employee_status_code = employee.status.value if employee.status else "A"  # Assuming "A" (Active) as default
        self.employee_status_effective_date = employee.termination_date.strftime('%Y%m%d') if employee.termination_date else "19000101"
        self.employee_service_date = employee.start_date.strftime('%Y%m%d') if employee.start_date else "19000101"
        self.rehire_date = employee.original_hire_date.strftime('%Y%m%d') if employee.original_hire_date else "19000101"
        self.original_hire_date = employee.original_hire_date.strftime('%Y%m%d') if employee.original_hire_date else "19000101"
        self.employment_type = "F" if employee.is_full_time else "P"
        self.exempt_non_exempt = "E" if employee.is_salaried else "N"
        self.benefit_salary_amount = "0000000V00"  # Default salary amount
        self.salary_basis = "A"  # Default to Annual
        self.salary_effective_date = "19000101"  # Default salary effective date
        self.job_title = employee.job_title or "Unknown Job Title"

    return employee_record
