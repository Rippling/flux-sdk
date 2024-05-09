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
    """
    original_pay_date: This field denotes the original pay date for the Payroll run
    """
    original_pay_date: Optional[datetime]
    """
    check_date: This field denotes the check date for the Payroll run
    """
    check_date: Optional[date]
    """
    paid_at_date: This field denotes the paid_at_date date for the Payroll run
    """
    paid_at_date: Optional[datetime]
    """
    check_date: This field denotes the run type [REGULAR, OFF_CYCLE ...] for the Payroll run
    """
    run_type: Optional[PayrollRunType]
    """
    pay_period_start_date: This field denotes pay period start date for the Payroll run
    """
    pay_period_start_date: Optional[datetime]
    """
    pay_period_end_date: This field denotes pay period end date for the Payroll run
    """
    pay_period_end_date: Optional[datetime]
    """
    payroll_run_name: This field denotes payroll run name for the Payroll run
    """
    payroll_run_name: Optional[str]
    """
    payroll_run_name: This field denotes payroll run frequency value [SEMI_MONTHLY, WEEKLY ..] for the Payroll run
    """
    pay_frequency: Optional[str]


class PayrollUploadSettings:
    """
    This is the one of the params for "format_contributions" and "format_contribution" method in the
    ReportPayrollContributions interface.
    """
    """
    env: This field denotes the app environments. TS denotes the Testing environment and AP denotes the live environment
         for the App
    """
    environment: str
    """
    vendor_id: This field denotes the unique vendor id of Rippling
    """
    vendor_id: str
    """
    ein: This field denotes the unique Employer Identification Number 
    """
    ein: str
    """
    company_legal_name: This field denotes the Company legal Name
    """
    company_legal_name: str
    """
    company_id: This field denotes the Company ID
    """
    company_id: str
    """
    payrun_info: This object contains the details of the Payroll run
    """
    payrun_info: PayrunInfo
    """
    customer_partner_settings: This dict contains the settings value specified on manifest in key-value pair
    """
    customer_partner_settings: dict
    """
    company_name: This field denotes the Company Name
    """
    company_name: str
    """
    current_month_payruns: This field denotes the current month payruns for the company
    """
    current_month_payruns: Optional[list[PayrunInfo]]


class PayrollRunContribution:
    """
    This contains payroll contribution amount corresponding to a particular deduction type for the employee.
    """
    deduction_type: ContributionType
    amount: Decimal


class EoyInfo:
    """
    This contains payroll contribution year to date of employee for all possible deduction types. If year to date
    deduction sum your app requires is not present please reach out to apps@rippling.com to add support for that
    particular deduction.
    """
    """
    year_to_date_pretax_deferral: This field contains the year to date pre-tax deferral contribution
    """
    year_to_date_pretax_deferral: Decimal
    """
    year_to_date_roth_deferral: This field contains the year to date roth deferral contribution
    """
    year_to_date_roth_deferral: Decimal
    """
    year_to_date_loan_payments: This field contains the year to date loan deferral contribution
    """
    year_to_date_loan_payments: Decimal
    """
    year_to_date_employer_match: This field contains the year to date employer match deferral contribution
    """
    year_to_date_employer_match: Decimal
    """
    year_to_date_gross_pay: This field contains the year to date gross pay
    """
    year_to_date_gross_pay: Decimal
    """
    year_to_date_hours: This dict contains the year to date total hours if the EmploymentType is Hourly
    """
    year_to_date_hours: Decimal
    """
    year_to_date_pretax_catchup: This dict contains the year to date total pre-tax catchup contribution
    """
    year_to_date_pretax_catchup: Decimal
    """
    year_to_date_roth_catchup: This dict contains the year to date total roth catchup contribution
    """
    year_to_date_roth_catchup: Decimal




class EmployeeDeduction:
    """
    This contains employee deduction details corresponding to a deduction type.
    """
    deduction_type: DeductionType
    is_percentage: bool
    amount: Decimal
    total_pay_for_percentage_contribution: Optional[Decimal]

class LeaveInfo:
    """
    This contains employee leave of absence details corresponding to a leave type.
    """
    leave_type: LeaveType
    start_date: date
    return_date: date
    is_paid: bool

class EmployeePayrollRecord:
    """
    This is the one of the params for "format_contributions" method in the ReportPayrollContributions
    interface.
    """
    """
    employee: This object contains details of the Employee
    """
    employee: Employee
    """
    employee: This object contains list of payroll run contributions
    """
    payroll_contributions: list[PayrollRunContribution]
    """
    employee: This object contains list of employee deductions 
    """
    employee_deductions: list[EmployeeDeduction]
    """
    employee: This field indicates if the employee is eligible
    """
    is_eligible: Optional[bool]
    """
    employee: This field indicates the salary of the employee
    """
    salary: Optional[Decimal]
    """
    last_payrun: This field indicates whether this is last payrun of the employee 
    """
    last_payrun: Optional[bool]
    qualifier: Optional[str]
    """
    base_pay: This field indicates the value of the base_pay for the employee
    """
    base_pay: Optional[Decimal]
    """
    gross_pay: This field indicates the value of the gross_pay for the employee
    """
    gross_pay: Optional[Decimal]
    """
    hours_worked: This field indicates the value of the hours_worked for the employee
    """
    hours_worked: Optional[Decimal]
    total_pay_for_percentage_deductions: Optional[Decimal]
    """
    annual_salary: This field indicates the value of the annual_salary for the employee
    """
    annual_salary: Optional[Decimal]
    """
    eoy_info: This field indicates the value of the eoy info for the employee
    """
    eoy_info: Optional[EoyInfo]
    """
    leave_info: This field indicates the value of the leave info for the employee for this payroll run
    """
    leave_infos: list[LeaveInfo]
    """
    ytd_leave_infos: This field indicates the value of the leave info for the employee ytd
    """
    ytd_leave_infos: list[LeaveInfo]
    """
    severance: This field indicates the value of the total severance for the employee for this payroll run
    """
    severance: Optional[Decimal]
    """
    bonus: This field indicates the value of the total bonus for the employee for this payroll run
    """
    bonus: Optional[Decimal]
    """
    imputed_pay: This field indicates the value of the total imputed pay for the employee for this payroll run
    """
    imputed_pay: Optional[Decimal]
