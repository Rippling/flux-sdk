from datetime import datetime
from enum import Enum
from typing import Optional

from flux_sdk.flux_core.data_models import Address, EmployeeState, Gender


class AppConfig:
    '''
    This contains the application data gathered durring installation which is necesary to prepare employee data or process deductions
    '''
    auto_enroll: bool
    group_id: str
    

class Name:
    title: Optional[str]
    first: str
    middle: Optional[str]
    last: str
    suffix: Optional[str]

    @property
    def full_name(self):
        return f"${self.first} ${self.last}"
    

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

class EmploymentHours:
    type: EmploymentType
    effectiveDate: datetime
    hours_per_week: Optional[int]

class Employment:
    hours: EmploymentHours
    is_rehire: bool
    termination_date: Optional[datetime]
    start_date: datetime
    original_hire_date: datetime
    w2_start_date: datetime
    pay: Pay
    

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

class EmployeeData:
    '''
    This contains the core data about an employee which is relevant to a ben admin provider
    '''
    id: str
    ssn: str
    name: Name
    dob : datetime
    phone_number: str
    business_email: str
    personal_email: str
    gender: Gender
    employment: Employment
    pay: Pay
    address: Address
    status: EmployeeStatus
    benefits: BenefitsEligibilityStatus
    
