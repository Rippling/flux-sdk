from datetime import date
from enum import Enum

from flux_sdk.flux_core.data_models import Address, Gender, Name


class DependentRelationship(Enum):
    """
    Describes the relationship of the member to the employee.
    """
    """The employee"""
    EMPLOYEE = "EMPLOYEE"
    """The spouse of the employee"""
    SPOUSE = "SPOUSE"
    """The domestic partner of the employee"""
    DOMESTIC_PARTNER = "DOMESTIC_PARTNER"
    """The child of the employee"""
    CHILD = "CHILD"
    """The ex-spouse of the employee"""
    EX_SPOUSE = "EX_SPOUSE"
    """The ex-domestic partner of the employee"""
    EX_DOMESTIC_PARTNER = "EX_DOMESTIC_PARTNER"


class BenefitsDependent:
    """
    This object contains the details of an individual enrolled in a benefit plan.
    """
    """The unique ID"""
    id: str
    """The name of the dependent"""
    name: Name
    """The social security number of the dependent"""
    ssn: str
    """The date of birth of the dependent"""
    dateOfBirth: date
    """The address of the dependent"""
    address: Address
    """The relationship of the dependent to the employee"""
    relationship: DependentRelationship
    """The gender of the dependent"""
    gender: Gender
    """Does the dependent smoke?"""
    smoker: bool
    """Is the dependent disabled?"""
    disabled: bool
    """IS the dependent a veteran?"""
    military: bool
    """Is the dependent court ordered to be enrolled?"""
    courtOrdered: bool


class BenefitsLineType(Enum):
    """
    Describes the type of benefit plan.
    """
    """Medical plan"""
    MEDICAL = "MEDICAL"
    """Dental plan"""
    DENTAL = "DENTAL"
    """Vision plan"""
    VISION = "VISION"
    """Short term disability plan"""
    SHORT_DISABILITY = "SHORT_DISABILITY"
    """Long term disability plan"""
    LONG_DISABILITY = "LONG_DISABILITY"
    """Life insurance plan"""
    LIFE = "LIFE"
    """Acc"""
    ACCIDENTAL_DEATH_AND_DISMEMBERMENT = "ACCIDENTAL_DEATH_AND_DISMEMBERMENT"
    """Supplemental life insurance plan"""
    SECONDARY_LIFE = "SECONDARY_LIFE"
    """Voluntary life insurance plan"""
    VOLUNTARY_LIFE = "VOLUNTARY_LIFE"
    """Critical illness plan"""
    CRITICAL_ILLNESS = "CRITICAL_ILLNESS"
    """Parking benefits"""
    PARKING = "PARKING"
    """Transit benefits"""
    TRANSIT = "TRANSIT"
    """Health savings account"""
    FSA = "FSA"
    """Health savings account"""
    HEALTH_SAVING = "HEALTH_SAVING"
    """Cancer insurance plan"""
    CANCER = "CANCER"
    """Accident insurance plan"""
    ACCIDENT = "ACCIDENT"
    """Hospital indemnity plan"""
    HOSPITAL = "HOSPITAL"
    """Employee assistance program"""
    EMPLOYEE_ASSISTANCE_PROGRAM = "EMPLOYEE_ASSISTANCE_PROGRAM"
    """Pet insurance plan"""
    PET_INSURANCE = "PET_INSURANCE"
    """Travel insurance"""
    TRAVEL_INSURANCE = "TRAVEL_INSURANCE"
    """"Legal aid benefit"""
    LEGAL_AID = "LEGAL_AID"
    """Identity theft protection"""
    IDENTITY_THEFT = "IDENTITY_THEFT"
    """Remote medical care"""
    TELEMEDICINE = "TELEMEDICINE"
    """Mental health benefits"""
    MENTAL_HEALTH = "MENTAL_HEALTH"
    """Fertility program"""
    FERTILITY = "FERTILITY"
    """Financial wellness program"""
    FINANCIAL_WELLNESS = "FINANCIAL_WELLNESS"
    """Primary care program"""
    PRIMARY_CARE = "PRIMARY_CARE"
    """Maternity benefits"""
    MATERNITY = "MATERNITY"
    """Care assistance"""
    CARE_NAVIGATION = "CARE_NAVIGATION"
    """Health reimbursement account"""
    HEALTH_REIMBURSEMENT = "HEALTH_REIMBURSEMENT"

class DependentLineDetails:
    """
    This object contains the details of an individual enrolled in a life benefit plan.
    """
    """The dependent unique ID"""
    dependentId: str
    """The amount of coverage for this dependent, is 0 on non-life lines"""
    baseCoverageVolume: float
    """The amount of voluntary coverage for this dependent, is 0 on non-life lines"""
    voluntaryCoverageVolume: float


class GroupingType(Enum):
    """No grouping type, plan waived"""
    NONE = "NONE"
    """Enrollment only includes the employee"""
    EMPLOYEE = "EMPLOYEE"
    """Enrollment includes the employee and their spouse"""
    EMPLOYEE_AND_SPOUSE = "EMPLOYEE_AND_SPOUSE"
    """Enrollment includes the employee and their children"""
    EMPLOYEE_AND_KIDS = "EMPLOYEE_AND_KIDS"
    """Enrollment includes the employee and their spouse and children"""
    EMPLOYEE_AND_FAMILY = "EMPLOYEE_AND_FAMILY"
    """Employee and one dependent (deprecated)"""
    EMPLOYEE_ONE = "EMPLOYEE_ONE"
    """Employee and two or more dependents (deprecated)"""
    EMPLOYEE_TWO_OR_MORE = "EMPLOYEE_TWO_OR_MORE"


class LineEnrollment:
    '''
    This object contains the details of an employee's enrollment
    in a single line of coverage.
    '''
    """The unique ID of the plan"""
    planId: str
    """The type of benefits"""
    lineType: BenefitsLineType
    """Date the coverage is effective"""
    effectiveDate: date
    """Date the coverage expires"""
    expirationDate: date
    """The dependents covered by this line"""
    enrolledDependents: list[DependentLineDetails]
    """The group type of the enrollment"""
    groupingType: GroupingType
    """Indicates if the employee is enrolled in COBRA"""
    isCobra: bool
    """Indicates if the employee has waived the plan"""
    isWaived: bool


class BenefitsPlan:
    """The details of a benefit plan"""
    """The unique ID of the plan"""
    id: str
    """The group ID of the plan"""
    groupId: str
    """The name of the plan"""
    planName: str



class EmployeeEnrollments:
    """This object contains the details of an employee's enrollments in benefit plans."""
    """The unique ID of the employee"""
    employeeId: str
    """The list of dependents in the employee's household"""
    dependents: list[BenefitsDependent]
    """The list of lines the employee is enrolled in"""
    enrollments: list[LineEnrollment]


class CompanyEnrollmentInfo:
    """All enrollment information for a company"""
    """The list of plans offered by the company"""
    plans: list[BenefitsPlan]
    """The list of employees and their enrollments"""
    employeeEnrollments: list[EmployeeEnrollments]
