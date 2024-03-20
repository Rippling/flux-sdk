from datetime import datetime
from enum import Enum
from typing import Optional

from flux_sdk.flux_core.data_models import Employee, EmployeeState


class ReportEmployeesPersonalAndEmploymentDataConfig:
    '''
    This contains the application data gathered durring installation
    which is necesary to prepare employee data or process deductions
    '''
    auto_enroll: bool
    group_number: str
    company_id: str
    

class EmploymentType(Enum):
    CONTRACTOR = 1
    SALARIED_FT = 2
    SALARIED_PT = 3
    HOURLY_FT = 4
    HOURLY_PT = 5
    TEMP = 6


class MonetaryValue:
    value: float
    currency_type: str


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


class Pay:
    frequency: PayFrequency
    frequency_effective_date: datetime
    time_unit: PayTimeUnit
    value_per_unit: MonetaryValue
    value_effective_date: datetime
    salary_or_equivalent: MonetaryValue
    expected_commission: Optional[MonetaryValue]

class EmploymentHours:
    type: EmploymentType
    type_effective_date: datetime
    hours_per_week: Optional[int]
    hours_effective_date: datetime

class TerminationType(Enum):
    VOLUNTARY = 0
    INVOLUNTARY = 1
    RETIREMENT = 2
    DEATH = 3
    ABANDONMENT = 4
    OFFER_DECLINE = 5
    RESCIND = 6
    RENEGE = 7

class Employment:
    hours: EmploymentHours
    pay: Pay
    is_rehire: bool
    termination_date: Optional[datetime]
    termination_type: Optional[TerminationType]
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


class EmployeePersonalAndEmploymentData:
    '''
    This contains the core data about an employee which is relevant to a benefits administration provider
    '''
    id: str
    employee_number: int
    company_tax_id: str
    personal: Employee
    employment: Employment
    pay: Pay
    status: EmployeeStatus
    benefits_eligibility: BenefitsEligibilityStatus
    
