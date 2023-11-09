from datetime import date
from enum import Enum
from typing import Optional

from flux_sdk.flux_core.data_models import Employee

class EmployeeEligibilityRecord:
    employee: Employee
    company_id: str
    start_date: date
    end_date: date
    dependent_first_name: Optional[str]
    dependent_last_name: Optional[str]
