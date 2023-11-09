from datetime import date
from enum import Enum
from typing import Optional


class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NON_BINARY = "NON_BINARY"
    DECLINE_TO_SELF_IDENTIFY = "DECLINE_TO_SELF_IDENTIFY"


class EmployeeEligibilityRecord:
    role_id: str
    company_id: str
    first_name: str
    last_name: str
    email: str
    start_date: date
    dob: date
    gender: Gender
    zip: str
    end_date: date
    dependent_first_name: Optional[str]
    dependent_last_name: Optional[str]
