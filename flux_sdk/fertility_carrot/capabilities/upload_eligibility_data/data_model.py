from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional


class EmployeeEligibilityRecord:
    role_id: str
    ssn: str
    employee_number: str
    contribution_date: date
    contribution_type: str
    contribution_amount: Decimal
    tax_year: Optional[str]
    employee: Optional[Employee]
