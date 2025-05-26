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
    """
    Data model representing an Employee contribution record.

    Attributes:
        role_id (str): Unique identifier for the employee's role.
        ssn (str): Employee's Social Security Number.
        employee_number (str): Unique identifier for the employee.
        plan_name (PlanType): Name/type of the insurance or benefits plan.
        contribution_date (date): Date when the contribution was made.
        contribution_type (str): Type of contribution.
        contribution_amount (Decimal): Amount of the contribution for the period.
        yearly_contribution_amount (Decimal): Total contribution amount for the year.
        tax_year (Optional[str]): Tax year the contribution is associated with.
        employee (Optional[Employee]): Reference to the employee record.
        fsa_plan_type (Optional[FSAPlanType]): Type of Flexible Spending Account plan, if applicable.
        enrollment (EmployeeEnrollment): Enrollment record associated with the contribution.
        employee_contribution (Optional[Decimal]): Portion of the contribution paid by the employee.
        employer_contribution (Optional[Decimal]): Portion of the contribution paid by the employer.
    """
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
    employee_contribution: Optional[Decimal]
    employer_contribution: Optional[Decimal]
