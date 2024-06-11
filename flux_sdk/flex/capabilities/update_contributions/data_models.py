from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional

from flux_sdk.flex.capabilities.update_enrollments.data_models import EmployeeEnrollment
from flux_sdk.flex.data_models.flex_models import FSAPlanType
from flux_sdk.flux_core.data_models import Employee


class PlanType(Enum):
    FSA_MEDICAL = 0
    FSA_DEPENDENT_CARE = 1
    HSA = 2
    COMMUTER_TRANSIT = 3
    COMMUTER_PARKING = 4


class EmployeeContribution:
    role_id: str
    ssn: str
    employee_number: str
    plan_name: PlanType
    contribution_date: date
    contribution_type: str
    contribution_amount: Decimal
    yearly_contribution_amount: Decimal
    tax_year: Optional[str]
    employee: Optional[Employee]
    fsa_plan_type: Optional[FSAPlanType]
    enrollment: EmployeeEnrollment
