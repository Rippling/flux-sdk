from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional

from flux_sdk.flex.data_models.flex_models import FSAPlanType


class BenefitType(Enum):
    FSA = 0
    HSA = 1
    COMMUTER = 2


# specify the family enrollment status for HSA
class HSAFamilyType(Enum):
    UNSPECIFIED = 0
    EE_ONLY = 1
    EE_AND_SPOUSE = 2
    EE_AND_SPOUSE_AND_ONE_OR_MORE_CHILDREN = 3
    EE_AND_ONE_CHILD = 4
    EE_AND_TWO_OR_MORE_CHILDREN = 5


class EmployeeEnrollment:
    role_id: str
    employee_number: str
    last_name: str
    first_name: str
    middle_name: Optional[str]
    gender: str
    marital_status: Optional[str]
    mothers_maiden_name: Optional[str]
    dob: date
    ssn: str
    address_line_1: str
    address_line_2: Optional[str]
    address_line_3: Optional[str]
    address_line_4: Optional[str]
    city: str
    state: str
    zip: str
    country: str
    home_phone: str
    work_phone: Optional[str]
    work_phone_ext: Optional[str]
    mobile_carrier: Optional[str]
    mobile_phone_number: str
    benefit_type: Optional[BenefitType]
    primary_email: str
    work_email: str
    role_start_date: date
    hours_per_week: str
    pay_frequency: str
    pay_frequency_effective_date: date
    role_status: str
    employee_state_effective_date: date
    final_payroll_process_date: date
    final_contribution_process_date: date
    time_zone: str
    deduction_count_per_plan_year: Optional[str]
    line_type: Optional[str]
    plan_name: str
    enrollment_effective_date: date
    enrollment_expiration_date: date
    employee_total_election_amount: Decimal
    employer_yearly_contribution_amount: Decimal
    employee_per_pay_period_deduction_amount: Decimal
    employer_per_pay_period_contribution_amount: Decimal
    election_amount_indicator: Optional[str]
    hdhp_coverage_level: Optional[str]
    plan_year_start_date: str  # DEPRECATE: the type is wrong, replaced by plan_year_valid_from_date
    plan_year_end_date: str  # DEPRECATE: the type is wrong, replaced by plan_year_valid_to_date
    plan_year_valid_from_date: date
    plan_year_valid_to_date: date
    division: str
    has_dependent: bool
    hsa_family_type: Optional[HSAFamilyType]
    fsa_plan_type: Optional[FSAPlanType]
    first_enrollment_date: Optional[date]
    department: Optional[str]
    hsa_annual_limit_type: Optional[str]
