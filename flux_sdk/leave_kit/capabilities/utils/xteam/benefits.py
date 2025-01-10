from enum import Enum
from typing import Optional
from datetime import date

class Gender(Enum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"

class MaritalStatus(Enum):
    SINGLE = "Single"
    MARRIED = "Married"
    DIVORCED = "Divorced"
    WIDOWED = "Widowed"
    OTHER = "Other"

class CoverageTier(Enum):
    EMPLOYEE_ONLY = 1
    EMPLOYEE_AND_FAMILY = 2
    EMPLOYEE_AND_SPOUSE = 3
    EMPLOYEE_AND_CHILDREN = 4

class Benefits:
    def __init__(
        self,
        member_ssn_or_id: str,
        relationship_code: str,
        last_name: str,
        first_name: str,
        middle_initial: Optional[str] = None,
        date_of_birth: date,
        marital_status: Optional[MaritalStatus] = None,
        gender: Optional[Gender] = None,
        mailing_address_1: str,
        mailing_address_2: Optional[str] = None,
        mailing_city: str,
        mailing_state: str,
        mailing_zip_code: str,
        mailing_country_code: int = 840,
        client_field_2: Optional[str] = None,
        client_field_3: Optional[str] = None,
        coverage_effective_date: Optional[date] = None,
        coverage_termination_date: Optional[date] = None,
        std_coverage_plan_option: Optional[float] = None,
        ltd_coverage_plan_option: Optional[float] = None,
        basic_life_face_amount: Optional[int] = None,
        basic_ad_d_face_amount: Optional[int] = None,
        supplemental_life_face_amount: Optional[int] = None,
        supplemental_ad_d_face_amount: Optional[int] = None,
        spouse_supplemental_life_face_amount: Optional[int] = None,
        dependent_child_supplemental_life_face_amount: Optional[int] = None,
        spouse_supplemental_ad_d_face_amount: Optional[int] = None,
        dependent_child_supplemental_ad_d_face_amount: Optional[int] = None,
        ci_benefit_amount: Optional[int] = None,
        coverage_tier: Optional[CoverageTier] = None,
        plan_number: Optional[str] = None,
        plan_option: Optional[str] = None
    ):
        self.member_ssn_or_id = self.validate_no_hyphens(member_ssn_or_id, "Member SSN/ID")
        self.relationship_code = relationship_code
        self.last_name = last_name
        self.first_name = first_name
        self.middle_initial = middle_initial
        self.date_of_birth = date_of_birth
        self.marital_status = marital_status
        self.gender = gender
        self.mailing_address_1 = mailing_address_1
        self.mailing_address_2 = mailing_address_2
        self.mailing_city = mailing_city
        self.mailing_state = mailing_state
        self.mailing_zip_code = self.validate_zip_code(mailing_zip_code)
        self.mailing_country_code = mailing_country_code
        self.client_field_2 = client_field_2
        self.client_field_3 = client_field_3
        self.coverage_effective_date = coverage_effective_date
        self.coverage_termination_date = coverage_termination_date
        self.std_coverage_plan_option = std_coverage_plan_option
        self.ltd_coverage_plan_option = ltd_coverage_plan_option
        self.basic_life_face_amount = basic_life_face_amount
        self.basic_ad_d_face_amount = basic_ad_d_face_amount
        self.supplemental_life_face_amount = supplemental_life_face_amount
        self.supplemental_ad_d_face_amount = supplemental_ad_d_face_amount
        self.spouse_supplemental_life_face_amount = spouse_supplemental_life_face_amount
        self.dependent_child_supplemental_life_face_amount = dependent_child_supplemental_life_face_amount
        self.spouse_supplemental_ad_d_face_amount = spouse_supplemental_ad_d_face_amount
        self.dependent_child_supplemental_ad_d_face_amount = dependent_child_supplemental_ad_d_face_amount
        self.ci_benefit_amount = ci_benefit_amount
        self.coverage_tier = coverage_tier
        self.plan_number = plan_number
        self.plan_option = plan_option

    @staticmethod
    def validate_no_hyphens(value: str, field_name: str) -> str:
        if "-" in value:
            raise ValueError(f"{field_name} must not contain hyphens.")
        return value

    @staticmethod
    def validate_zip_code(zip_code: str) -> str:
        if not re.match(r'^\d{5}(-\d{4})?$', zip_code):
            raise ValueError("Invalid ZIP Code format. Use xxxxx or xxxxx-xxxx.")
        return zip_code
