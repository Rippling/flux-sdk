from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Optional

from flux_sdk.flux_core.data_models import (
    Department,
    Employee,
    EmployeeState,
    EmploymentType,
    PayFrequency,
    PayTimeUnit,
    TerminationType,
    WorkLocation,
)


class ReportEmployeesHrDataConfig:
    '''
    This contains the application data gathered durring installation
    which is necesary to prepare employee data or process deductions
    '''
    """ Whether or not the company auto enrolls employee's in company paid plans"""
    auto_enroll: bool
    """ The unique identifier of the company in Rippling"""
    company_id: str
    """ Any app settings that are configured per fein """
    fein_settings: dict[str, dict[str, Any]]
    """ Any settings unique to the partner company """
    customer_partner_settings: dict[str, Any]


class MonetaryValue:
    """ Object describing a value in a specific currency """
    """ A value of currency """
    value: Decimal
    """ The type of currency"""
    currency_type: str


class Pay:
    """ Object describing how the employee is paid """
    """ How often they are paid """
    frequency: PayFrequency
    """ The date that their pay frequency took effect """
    frequency_effective_date: datetime
    """ The unit of time on which the employee is paid"""
    time_unit: PayTimeUnit
    """ The amount paid per time unit """
    value_per_unit: MonetaryValue
    """ The date their pay value first took effect """
    value_effective_date: datetime
    """ The salary value, or  """
    salary_or_equivalent: MonetaryValue
    """ The value the employee expects in commission, if commission is possible """
    expected_commission: MonetaryValue | None
    """ The value the employee expects in bonus """
    expected_bonus: MonetaryValue | None

class EmploymentHours:
    """ Object describing the employees working hours """

    """ Describes the hours and pay structure of the employee """
    type: EmploymentType
    """ The date that the employee took on this employment type """
    type_effective_date: datetime
    """ Deprecated - The expected hours per week, if hourly """
    hours_per_week: int | None
    """ The expected hours per week, if hourly """
    hours_per_week_v2: float | None
    """ The date the employee began this hours schedule """
    hours_effective_date: datetime

class JobDetails:
    """ This object contains details about the employees current job as required by the Ben Admin Apps"""

    """ The employees job title """
    title: Optional[str]
    """ The date the employee took on this job title """
    job_effective_date: Optional[datetime]
    """ The employees department """
    department: Optional[Department]
    """ The employees location """
    location: Optional[WorkLocation]
    """ The Company Configured Employment Type"""
    company_employment_type: Optional[str]


class Employment:
    """ Object describing the employees employment contract """

    """ Describes the working hours of the employee """
    hours: EmploymentHours
    """ Describes the employees pay """
    pay: Pay
    """ If the employee has left the company and then been rehired """
    is_rehire: bool
    """ Job details of the employee """
    job_details: Optional[JobDetails]
    """ The last date the employee is with the company, if leaving/left """
    termination_date: datetime | None
    """ The reason the employee is leaving the company, if leaving/left """
    termination_type: TerminationType | None
    """ The date the employee started or returned with the company """
    start_date: datetime
    """ The first date the employee started with the company """
    original_hire_date: datetime
    """ The date the employee will begin to be paid with the company """
    w2_start_date: datetime
    """ The permanent profile number - unique across rehired roles at same company """
    permanent_profile_number: Optional[str]
    

class BenefitsEligibility(Enum):
    # this will expand to cover cobra later
    ELIGIBLE = 1
    IN_ELIGIBLE = 2

class BenefitsEligibilityStatus:
    """ Describes the employees eligibility for benefits """
    eligibility: BenefitsEligibility
    """ The date that this status began for the employee """
    effective_date: datetime

class EmployeeStatus:
    """ The employees employment status """
    status: EmployeeState
    """ The date when the employee entered this status """
    effective_date: datetime

class VendorCustomFields:
    field_name: str
    field_value: str

class EmployeeHrData:
    '''
    This contains the core data about an employee
    which is relevant to a benefits administration provider
    '''
    """ The employee's unique identifier in Rippling """
    id: str
    """ The employee's number with the company """
    employee_number: int
    """ The companies policy group number which the employee is included in """
    group_number: str
    """ The employee's class code """
    class_code: Optional[str]
    """ The company tax id (ein) that applies to the employee """
    company_tax_id: str
    """ An object containing the personal details of the employee """
    personal: Employee
    """ An object containing the details of the employees employement """
    employment: Employment
    """ An object containing hte details of the employees pay for their employment """
    pay: Pay
    """ An object describing the employees employment status """
    status: EmployeeStatus
    """ Whether or not the employee is considered eligible for benefits """
    benefits_eligibility: BenefitsEligibilityStatus
    """ Dynamic Fields for the Vendor """
    vendor_custom_fields: list[VendorCustomFields]





