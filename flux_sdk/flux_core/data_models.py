from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Optional


class LeaveType(Enum):
    VACATION = 1
    WFH = 2
    JURY_DUTY = 3
    BEREAVEMENT = 4
    PERSONAL_DAYS = 5
    UNPAID = 6
    ERC = 7
    CUSTOM = 8
    PARENTAL_LEAVE = 9
    OTHER_LEAVE_OF_ABSENCE = 10
    MEDICAL = 11
    MILITARY = 12

class LeaveInfo:
    """
    This contains employee leave of absence details corresponding to a leave type.
    """
    leave_type: LeaveType
    start_date: date
    return_date: date
    is_paid: bool

class MonetaryValue:
    """
    Object describing a value in a specific currency
    """

    """ A value of currency, for ex, the '5' in 5 USD """
    value: Decimal
    
    """ The type of currency, for ex, 'USD' """
    currency_type: str

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


class MaritalStatus(Enum):
    """
    Developers are expected to use this to fill martial status of employee inside the file.
    """
    SINGLE = 0
    MARRIED = 1
    DIVORCED = 2
    WIDOWED = 3
    PERMANENTLY_SEPARATED = 4
    REGISTERED_PARTNERSHIP = 5

class PhoneNumber:
    """
    This contains the details of an international phone number.
    """
    country_code: str
    national_number: str
    extension: Optional[str]


class Employee:
    """
    This contains all the details about the employee including personal and job details. Developers are expected to
    use to fill employee details inside the file. If an employee attribute your app requires is
    not present please reach out to apps@rippling.com to add support for that attribute.
    """
    ssn: str
    role_id: str
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
    termination_date: Optional[date]
    w2_start_date: datetime
    address: Address
    status: EmployeeState
    dob: datetime
    phone_number: str
    phone_number_v2: PhoneNumber
    is_temporary: bool
    is_hourly: bool
    is_salaried: bool
    is_contractor: bool
    is_full_time: bool
    is_part_time: bool
    is_new_hire: bool
    is_rehire: bool
    is_international_employee: bool
    marital_status: Optional[MaritalStatus]
    employment_type: Optional[str] # The employment type of the employee.
    department: Optional[str]   # The department of the employee.
    termination_reason: Optional[str]   # The termination reason of the employee if the employee is terminated.
    work_location_nickname: Optional[str]
    teams: Optional[list[str]]
    company_employment_type_label: Optional[str]

class WorkLocation:
    """
    This contains the details of the work location of an employee.
    """

    """ Location code of the work location """
    location_code: Optional[str]
    """ City of the work location """
    city: Optional[str]
    """ State of the work location """
    state: Optional[str]
    """ Zip code of the work location """
    zip_code: Optional[str]
    """ Date since when the employee has been working at this location """
    effective_date: Optional[datetime]
    """ Nickname of work location """
    nickname: Optional[str]

class Department:
    """
    This contains the details of a department.
    """

    """ Reference code of the department """
    department_reference_code: Optional[str]
    """ Name of the department """
    name: Optional[str]
    """ Date since when the employee has been working in this department """
    effective_date: Optional[datetime]



class ContributionType(Enum):
    """
    This enum is an exhaustive list of all 401k Contribution types supported by Rippling. Developers are expected
    to use this to fetch the Employee deduction contribution based on contribution type. If a contribution type your app
    requires is not present please reach out to apps@rippling.com to add support for that particular deduction.
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
    _401K_CATCHUP = 10
    ROTH_401K_CATCHUP = 11
    ROTH_403B = 12
    _457B = 13
    ROTH_457B = 14
    COMPANY_MATCH_403B = 15
    COMPANY_MATCH_ROTH_403B = 16
    COMPANY_MATCH_457B = 17
    COMPANY_MATCH_ROTH_457B = 18
    SIMPLE_IRA = 19
    COMPANY_MATCH_SIMPLE_IRA = 20
    EMERGENCY_SAVINGS_ACCOUNT = 21
    COMPANY_MATCH_EMERGENCY_SAVINGS_ACCOUNT = 22

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
    _401K_CATCHUP = 5
    ROTH_401K_CATCHUP = 6
    ROTH_403B = 7
    _457B = 8
    ROTH_457B = 9
    SIMPLE_IRA = 10
    EMERGENCY_SAVINGS_ACCOUNT = 11


class PayrollRunType(Enum):
    """
    This enum is an exhaustive list of all payroll run types supported by Rippling. Developers are expected to use this
    to make decisions for file attributes based on run type.
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
    BULK_TERMINATION = 20


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

class ReportRow:
    """
    Represents each row in a report exported data.
    """

    fields: dict[str, Any]

class ReportData:
    """
    This contains the export of the report.
    """

    rows: list[ReportRow]

class AppContext:
    """
    This is the one of the params for "get_formatted_enrollments_files" method in the UpdateEnrollments
    interface.
    """
    """
    env: This field denotes the app enviroments. TS denotes the Testing enviroment and AP denotes the live enviroment 
         for the App
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


class EmploymentType(Enum):
    CONTRACTOR = 1
    SALARIED_FT = 2
    SALARIED_PT = 3
    HOURLY_FT = 4
    HOURLY_PT = 5
    TEMP = 6


class PayFrequency(Enum):
    WEEKLY = 1
    BI_WEEKLY = 2
    MONTHLY = 3
    SEMI_MONTHLY = 4
    QUARTERLY = 5
    ANNUALLY = 6


class PayTimeUnit(Enum):
    HOUR = 1
    DAY = 2
    WEEK = 3
    MONTH = 4
    YEAR = 5
    PAY_PERIOD = 6


class TerminationType(Enum):
    VOLUNTARY = 0
    INVOLUNTARY = 1
    RETIREMENT = 2
    DEATH = 3
    ABANDONMENT = 4
    OFFER_DECLINE = 5
    RESCIND = 6
    RENEGE = 7


class AppDisconnectedError(Exception):
    """
    This exception is raised when the app is disconnected from the third-party system.
    """
    pass

class Name:
    """
    This contains the details of an employee's name.
    """
    first: str
    """ The middle name of the employee """
    middle: Optional[str]
    """ The last name of the employee """
    last: str
    """ The suffix of the employee """
    suffix: Optional[str]
    """ The prefix of the employee """
    title: Optional[str]
