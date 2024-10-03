from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Optional

from flux_sdk.flux_core.data_models import (
    Employee,
    EmployeeState,
    EmploymentType,
    PayFrequency,
    PayTimeUnit,
    TerminationType,
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

class EmploymentHours:
    """ Object describing the employees working hours """

    """ Describes the hours and pay structure of the employee """
    type: EmploymentType
    """ The date that the employee took on this employment type """
    type_effective_date: datetime
    """ The expected hours per week, if hourly """
    hours_per_week: int | None
    """ The date the employee began this hours schedule """
    hours_effective_date: datetime


class Employment:
    """ Object describing the employees employment contract """

    """ Describes the working hours of the employee """
    hours: EmploymentHours
    """ Describes the employees pay """
    pay: Pay
    """ If the employee has left the company and then been rehired """
    is_rehire: bool
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
    """ The employee's social security number """
    ssn: Optional[str]
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
