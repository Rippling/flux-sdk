from datetime import datetime
from decimal import Decimal
from enum import Enum

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
    auto_enroll: bool
    group_number: str
    company_id: str


class MonetaryValue:
    value: Decimal
    currency_type: str


class Pay:
    frequency: PayFrequency
    frequency_effective_date: datetime
    time_unit: PayTimeUnit
    value_per_unit: MonetaryValue
    value_effective_date: datetime
    salary_or_equivalent: MonetaryValue
    expected_commission: MonetaryValue | None

class EmploymentHours:
    type: EmploymentType
    type_effective_date: datetime
    hours_per_week: int | None
    hours_effective_date: datetime


class Employment:
    hours: EmploymentHours
    pay: Pay
    is_rehire: bool
    termination_date: datetime | None
    termination_type: TerminationType | None
    start_date: datetime
    original_hire_date: datetime
    w2_start_date: datetime
    

class BenefitsEligibility(Enum):
    # this will expand to cover cobra later
    ELIGIBLE = 1
    IN_ELIGIBLE = 2

class BenefitsEligibilityStatus:
    eligibility: BenefitsEligibility
    effective_date: datetime

class EmployeeStatus:
    status: EmployeeState
    effective_date: datetime


class EmployeeHrData:
    '''
    This contains the core data about an employee
    which is relevant to a benefits administration provider
    '''
    id: str
    employee_number: int
    company_tax_id: str
    personal: Employee
    employment: Employment
    pay: Pay
    status: EmployeeStatus
    benefits_eligibility: BenefitsEligibilityStatus
    
