from datetime import date
from enum import Enum

from flux_sdk.flux_core.data_models import Address, Employee, Gender, Name


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
    """AD&D with voluntary buyup"""
    VOLUNTARY_ACCIDENTAL_DEATH_AND_DISMEMBERMENT = "VOLUNTARY_ACCIDENTAL_DEATH_AND_DISMEMBERMENT"
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
    """The unique id of the enrollment event that created this line enrollment"""
    eventId: str


class BenefitsPlan:
    """The details of a benefit plan"""
    """The unique ID of the plan"""
    id: str
    """The group ID of the plan"""
    groupId: str
    """The name of the plan"""
    planName: str

class EnrollmentEventReason(Enum):
    """The reasons an enrollment event can occur"""
    """The employee is newly hired"""
    NEW_HIRE = "NEW_HIRE"
    """The company has an open enrollment event"""
    OPEN_ENROLLMENT = "OPEN_ENROLLMENT"
    """The company has a new group enrollment event"""
    NEW_GROUP_ENROLLMENT = "NEW_GROUP_ENROLLMENT"
    """The company transfered benefits into Rippling"""
    BENEFITS_TRANSFER = "BENEFITS_TRANSFER"
    """The company canceled a line(s) of coverage"""
    GROUP_COVERAGE_CANCELATION = "GROUP_COVERAGE_CANCELATION"
    """Manual correction to the employee's enrollment"""
    MANUAL_CORRECTION = "MANUAL_CORRECTION"
    """The employee is newly married"""
    MARRIED = "MARRIED"
    """The employee has a new child"""
    NEW_CHILD = "NEW_CHILD"
    """The employee has a new adopted child"""
    ADOPTED_CHILD = "ADOPTED_CHILD"
    """The employee gets divorced"""
    DIVORCE = "DIVORCE"
    """The employee is legal separated from domestic partner"""
    LEGAL_SEPARATION = "LEGAL_SEPARATION"
    """The employee passes away"""
    DEATH = "DEATH"
    """The employee is newly guardian"""
    NEWLY_GUARDIAN = "NEWLY_GUARDIAN"
    """The employee has a new foster child"""
    NEW_FOSTER_CHILD = "NEW_FOSTER_CHILD"
    """The employee has a new domestic partnership"""
    NEW_DOMESTIC_PARTNERSHIP = "NEW_DOMESTIC_PARTNERSHIP"
    """The employee moves to a new location"""
    MOVED = "MOVED"
    """The employee has lost coverage from outside the company"""
    LOST_COVERAGE = "LOST_COVERAGE"
    """The employee's dependent has lost coverage outside the company"""
    DEPENDENT_LOST_COVERAGE = "DEPENDENT_LOST_COVERAGE"
    """The employee's dependent has gained coverage outside the company"""
    DEPENDENT_GAINED_COVERAGE = "DEPENDENT_GAINED_COVERAGE"
    """The employee has moved outside the USA"""
    DEPENDENT_MOVED_OUTSIDE_USA = "DEPENDENT_MOVED_OUTSIDE_USA"
    """The employee has been court ordered to enroll a dependent"""
    COURT_ORDERED = "COURT_ORDERED"
    """The employee has a new green card"""
    NEW_GREEN_CARD = "NEW_GREEN_CARD"
    """The employee has enrolled in coverage through a dependent"""
    ENROLLING_IN_DEPENDENT_COVERAGE = "ENROLLING_IN_DEPENDENT_COVERAGE"
    """The employee is enrolling in coverage outside the company"""
    ENROLLING_OTHER_COVERAGE = "ENROLLING_OTHER_COVERAGE"
    """The employee's dependents other benefit costs have changed"""
    DEPENDENT_COVERAGE_COST_CHANGED = "DEPENDENT_COVERAGE_COST_CHANGED"
    """The companies broker has changed"""
    BROKER_CHANGE = "BROKER_CHANGE"
    """The employee has a Covid-19 related enrollment"""
    COVID_19 = "COVID_19"
    """The employee has FSA changes due to COVID-19"""
    FSA_COVID_19 = "FSA_COVID_19"
    """The employee has a midyear enrollment due to COVID-19"""
    COVID_19_MIDYEAR_ENROLLMENT = "COVID_19_MIDYEAR_ENROLLMENT"
    """NDT has changed"""
    NDT_CHANGE = "NDT_CHANGE"
    """The employee's dependent has aged out of dependent coverage"""
    AGE_OUT_DEPENDENT = "AGE_OUT_DEPENDENT"
    """The employee changed hours to full time"""
    CHANGE_TO_FULL_TIME = "CHANGE_TO_FULL_TIME"
    """The employee voluntarily terminated their employment"""
    VOLUNTARY_TERMINATION = "VOLUNTARY_TERMINATION"
    """The employee was terminated by the company"""
    INVOLUNTARY_TERMINATION = "INVOLUNTARY_TERMINATION"
    """The employee is retiring"""
    RETIREMENT = "RETIREMENT"
    """The employee abandoned their employment"""
    ABANDON_EMPLOYMENT = "ABANDON_EMPLOYMENT"
    """The employee declined an open offer"""
    OFFER_DECLINED = "OFFER_DECLINED"
    """The employer rescinded a previously extended offer"""
    RESCIND_EMPLOYMENT_OFFER = "RESCIND_EMPLOYMENT_OFFER"
    """The employee canceled a previously accepted offer"""
    RENEGE_EMPLOYEMENT = "RENEGE_EMPLOYEMENT"
    """The employee has changed to part time hours"""
    CHANGE_TO_PART_TIME = "CHANGE_TO_PART_TIME"
    """The reason cannot be found"""
    UNKNOWN = "UNKNOWN"

class EnrollmentEvent:
    """The event that created an enrollment"""
    """The unique ID of the event"""
    eventId: str
    """The date of the event"""
    eventDate: date
    """The reason for the event"""
    eventReason: EnrollmentEventReason


class EmployeeEnrollments:
    """This object contains the details of an employee's enrollments in benefit plans."""
    """The unique ID of the employee"""
    employeeId: str
    """The list of dependents in the employee's household"""
    dependents: list[BenefitsDependent]
    """The list of lines the employee is enrolled in"""
    enrollments: list[LineEnrollment]
    """The list of events that created enrollments"""
    events: list[EnrollmentEvent]


class CompanyEnrollmentInfo:
    """All enrollment information for a company"""
    """The list of plans offered by the company"""
    plans: list[BenefitsPlan]
    """The list of employees and their enrollments"""
    employeeEnrollments: list[EmployeeEnrollments]


class CustomMapping:
    """
    A data model representing the mapping of plan names to their respective IDs and benefit tiers.

    Attributes:
        plan_name (str): The name of the plan.
        plan_id (str): The unique identifier for the plan.
        benefit_tier (str): The benefit tier associated with the plan.
    """
    plan_id: str
    plan_name: str
    benefit_tier: GroupingType
    benefit_tier_name: str


class CobraEmployeeEnrollment:
    """
    Represents the enrollments of an employee and their dependents in a COBRA plan.

    Attributes:
        employee (Employee): The employee who is enrolling in the COBRA plan.
        dependents (list[BenefitsDependent]): A list of dependents who are also enrolling in the COBRA plan.
        enrollment_event (EnrollmentEvent): The event that triggered the enrollment.
        line (LineEnrollment): The specific line of enrollment for the employee.
        plan (CustomMapping): The mapping of the plan name for the enrollment.
    """
    employee: Employee
    dependents: list[BenefitsDependent]
    enrollment_event: EnrollmentEvent
    line: LineEnrollment
    plan: CustomMapping
