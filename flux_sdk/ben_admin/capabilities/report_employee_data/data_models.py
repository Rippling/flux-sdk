from datetime import datetime
from enum import Enum
from typing import Optional

from flux_sdk.flux_core.data_models import Address, EmployeeState, Gender, MaritalStatus


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
    

class EmployementType(Enum):
    CONTRACTOR = 1
    SALARIED_FT = 2
    SALARIED_PT = 3
    HOURLY_FT = 4
    HOURLY_PT = 5
    TEMP = 6


class Employment:
    type: EmployementType
    is_rehire: bool
    termination_date: Optional[datetime]
    start_date: datetime
    start_date: datetime
    original_hire_date: datetime


class Pay:
    w2_start_date: datetime

class EmployeeData:
    '''
    This extends the core definition of an employee to include insurance eligibiliity data
    '''
    id: str
    ssn: str
    name: Name
    insurance_eligible: bool
    business_email: str
    personal_email: str
    gender: Gender
    employment: Employment
    pay: Pay
    address: Address
    status: EmployeeState
    dob : datetime
    phone_number: str
    marital_status: Optional[MaritalStatus]
    
