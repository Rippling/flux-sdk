from datetime import datetime
from enum import Enum
from typing import Optional


class EmployeeState(Enum):
    """
    This enum is an exhaustive list of all employee status types supported by Rippling. Developers are expected to
    use this make decisions for file attributes based on employee status.
    """
    INIT = 1
    HIRED = 2
    ACCEPTED = 3
    TERMINATED = 4
    ACTIVE = 5


class Address:
    """
    This contains the address details. Developers are expected to use this to fill location information
    inside the file.
    """
    address_line_1: str
    address_line_2: str
    city: str
    state: str
    zip_code: str
    country: Optional[str]


class Gender(Enum):
    """
    Developers are expected to use this to fill gender information inside the file.
    """
    MALE = 0
    FEMALE = 1
    NON_BINARY = 2
    DECLINE_TO_SELF_IDENTIFY = 3


class MaritalStatus:
    """
    Developers are expected to use this to fill martial status of employee inside the file.
    """
    SINGLE = 0
    MARRIED = 1
    DIVORCED = 2
    WIDOWED = 3
    PERMANENTLY_SEPARATED = 4
    REGISTERED_PARTNERSHIP = 5


class Employee:
    """
    This contains all the details about the employee including personal and job details. Developers are expected to
    use to fill employee details inside the file. If an employee attribute your app requires is
    not present please reach out to apps@rippling.com to add support for that attribute.
    """
    ssn: str
    first_name: str
    middle_name: str
    last_name: str
    employee_id: Optional[str]
    employee_number: Optional[int]
    job_title: Optional[str]
    start_date: datetime
    original_hire_date: datetime
    business_email: str
    personal_email: str
    gender: Gender
    termination_date: Optional[datetime]
    start_date: datetime
    w2_start_date: datetime
    address: Address
    status: EmployeeState
    dob : datetime
    phone_number: str
    is_temporary: bool
    is_hourly: bool
    is_salaried: bool
    is_contractor: bool
    is_full_time: bool
    is_part_time: bool
    is_new_hire: bool
    is_rehire: bool
    is_international_employee: bool
    martial_status: MaritalStatus


class ContributionType(Enum):
    """
    This enum is an exhaustive list of all 401k Contribution types supported by Rippling. Developers are expected
    to use this to fetch the Employee deduction contribution based on contribution type. If a contribution type your app requires is
    not present please reach out to apps@rippling.com to add support for that particular deduction.
    """
    _401K = 1
    ROTH = 2
    AFTER_TAX_401K = 3
    _403B = 4
    COMPANY_MATCH = 5
    COMPANY_MATCH_401K = 6
    COMPANY_MATCH_ROTH = 7
    COMPANY_MATCH_AFTER_TAX = 8
    LOAN = 9

class DeductionType(Enum):
    """
    This enum is an exhaustive list of all 401k deduction types supported by Rippling. Developers are expected
    to create EmployeeDeductionSetting with deduction_type being among this list. If a deduction your app requires is
    not present please reach out to apps@rippling.com to add support for that particular deduction.
    """

    _401K = 0
    ROTH_401K = 1
    _401K_LOAN_PAYMENT = 2
    AFTER_TAX_401K = 3
    _403B = 4


class PayrollRunType(Enum):
    """
    This enum is an exhaustive list of all payroll run types supported by Rippling. Developers are expected to use this to
    make decisions for file attributes based on run type.
    """
    INIT = 1
    REGULAR = 2
    OFF_CYCLE = 3
    CORRECTION = 4
    TERMINATION = 5
    RECONCILIATION = 6
    SEVERANCE = 7
    NEW_HIRE = 8
    POP = 9
    TRANSITION = 10
    CORRECTION_DISPLAY = 11
    EXCESS_HOURS = 12
    REIMBURSEMENT_SWEEP = 13
    SIGN_ON_BONUS = 14
    S_CORP = 15
    FRINGE_BENEFITS = 16
    CONTRACTOR_LATE_PAYMENTS = 17
    QUARTERLY_WAGE_RECONCILIATION = 18
    QUARTERLY_CORRECTION = 19

class OperatingMode(Enum):
    TEST = "TEST"
    LIVE = "LIVE"

class CompanyInfo:
    company_id: str
    company_name: str
    third_party_employer_code: str
    operating_mode: OperatingMode
    environment: Optional[str]
    ein: Optional[str]
    company_app_settings: Optional[dict]


class File:
    name: str
    content: bytes

class AppContext:
    """
    This is the one of the params for "get_formatted_enrollments_files" method in the UpdateEnrollments
    interface.
    """
    """
    env: This field denotes the app enviroments. TS denotes the Testing enviroment and AP denotes the live enviroment for the App
    """
    environment: str
    """
    vendor_id: This field denotes the unique vendor id of Rippling
    """
    vendor_id: str
    """
    ein: This field denotes the unique Employer Identification Number 
    """
    ein: str
    """
    company_legal_name: This field denotes the Company legal Name
    """
    company_legal_name: str
    """
    customer_partner_settings: This dict contains the settings value specified on manifest in key-value pair
    """
    customer_partner_settings: dict

