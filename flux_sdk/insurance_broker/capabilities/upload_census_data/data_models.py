from typing import Optional


class MemberData:
    """
    Data model representing a member's census information for insurance broker census data uploads.

    Attributes:
        company_name (str): Name of the company.
        company_id (str): Unique identifier for the company.
        company_ein (str): Employer Identification Number.
        first_name (str): Member's first name.
        middle_name (str): Member's middle name.
        last_name (str): Member's last name.
        subscriber_email (Optional[str]): Subscriber's email address.
        employee_ssn (str): Employee's Social Security Number.
        relationship (str): Relationship to the subscriber.
        gender (str): Gender of the member.
        dob (str): Date of birth.
        member_ssn (str): Member's Social Security Number.
        employee_cell_phone (Optional[str]): Employee's cell phone number.
        address_line_1 (str): Primary address line.
        address_line_2 (str): Secondary address line.
        city (str): City of residence.
        state (str): State of residence.
        zip (str): ZIP code.
        hire_date (Optional[str]): Date of hire.
        title (Optional[str]): Job title.
        employment_type (Optional[str]): Type of employment.
        hours (Optional[str]): Number of hours worked.
        earnings (Optional[str]): Earnings amount.
        salary (Optional[str]): Salary amount.
        work_location (Optional[str]): Work location.
        employee_class (Optional[str]): Employee class.
        pay_cycle (Optional[str]): Pay cycle.
        plan_type (str): Type of insurance plan.
        carrier_name (str): Name of the insurance carrier.
        plan_name (str): Name of the insurance plan.
        plan_enrollment_date (str): Date of plan enrollment.
        coverage_tier (str): Coverage tier.
        coverage_details (str): Details about coverage.
        action (str): Action to be taken (e.g., add, terminate).
        employee_rate (str): Employee's rate.
        employer_rate (str): Employer's rate.
        total_rate (str): Total rate.
        smoker (str): Smoking status.
        role_status (str): Role status.
        plan_effective_date (str): Effective date of the plan.
        plan_deduction_frequency (str): Frequency of plan deductions.
    """
    company_name: str
    company_id: str
    company_ein: str
    first_name: str
    middle_name: str
    last_name: str
    subscriber_email: Optional[str]
    employee_ssn: str
    relationship: str
    gender: str
    dob: str
    member_ssn: str
    employee_cell_phone: Optional[str]
    address_line_1: str
    address_line_2: str
    city: str
    state: str
    zip: str
    hire_date: Optional[str]
    title: Optional[str]
    employment_type: Optional[str]
    hours: Optional[str]
    earnings: Optional[str]
    salary: Optional[str]
    work_location: Optional[str]
    employee_class: Optional[str]
    pay_cycle: Optional[str]
    plan_type: str
    carrier_name: str
    plan_name: str
    plan_enrollment_date: str
    coverage_tier: str
    coverage_details: str
    action: str
    employee_rate: str
    employer_rate: str
    total_rate: str
    smoker: str
    role_status: str
    plan_effective_date: str
    plan_deduction_frequency: str
