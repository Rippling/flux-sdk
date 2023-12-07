from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional


class BenefitType(Enum):
    FSA = 0
    HSA = 1
    COMMUTER = 2


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
    election_amount_indicator: Optional[str]
    hdhp_coverage_level: Optional[str]
    plan_year_start_date: str
    division: str
    has_dependent: bool
    # the following field reads the value from
    # https://github.com/Rippling/rippling-protos/blob/d425ea95bb6d5fd220c4a7ad86adef67e966046f/protos/flex_benefits_platform/third_party_flex/v1/company_benefit_records.proto#L42
    hsa_family_type: Optional[HSAFamilyType]
