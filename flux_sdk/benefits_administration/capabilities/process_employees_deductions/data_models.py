from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from flux_sdk.flux_core.data_models import (
    ContributionType,
    DeductionType,
    Employee,
    LeaveType,
    PayrollRunType,
)


class PayrunInfo:
    """
    This is the one of the params for "format_contributions" method in the ReportPayrollContributions
    interface.
    """
    """
    payroll_run_id: This field denotes the unique payrun id for the Payroll run
    """
    payroll_run_id: str
    original_pay_date: Optional[datetime]
    check_date: Optional[datetime]
    paid_at_date: Optional[datetime]
    run_type: Optional[PayrollRunType]
    pay_period_start_date: Optional[datetime]
    pay_period_end_date: Optional[datetime]
    payroll_run_name: Optional[str]
    pay_frequency: Optional[str]


class DeductionType:
    MEDICAL = 7
    DENTAL = 8
    VISION = 9
    LIFE = 10
    SHORT_DISABILITY = 11
    LONG_DISABILITY = 12
    CRITICAL_ILLNESS = 13
    ACCIDENT = 14
    SECONDARY_LIFE = 15
    VOLUNTARY_LIFE = 16

class PayrollRunContribution:
    """
    This contains payroll contribution amount corresponding to a particular deduction type for the employee.
    """
    deduction_type: ContributionType
    amount: Decimal


class EmployeeDeduction:
    """
    This contains employee deduction details corresponding to a deduction type.
    """
    deduction_type: DeductionType
    is_percentage: bool
    amount: Decimal
    total_pay_for_percentage_contribution: Optional[Decimal]
    imputed_income: Decimal

