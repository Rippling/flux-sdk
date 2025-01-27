from datetime import date
from enum import Enum
from typing import Union

from flux_sdk.flux_core.data_models import Address, Gender, Name


class MemberRelationship(Enum):
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

class BenefitsMember:
    """
    This object contains the details of an individual enrolled in a benefit plan.
    """
    """The unique ID"""
    id: str
    """The name of the member"""
    name: Name
    """The social security number of the member"""
    ssn: str
    """The date of birth of the member"""
    dateOfBirth: date
    """The address of the member"""
    address: Address
    """The relationship of the member to the employee"""
    relationship: MemberRelationship
    """The gender of the member"""
    gender: Gender
    """Does the member smoke?"""
    smoker: bool
    """Is the member disabled?"""
    disabled: bool
    """IS the member a veteran?"""
    military: bool
    """Is the member court ordered to be enrolled?"""
    courtOrdered: bool

class BenefitsLineType(Enum):
    """
    Describes the type of benefit plan.
    """
    """Medical"""
    MEDICAL = "MEDICAL"
    """Dental"""
    DENTAL = "DENTAL"
    """Vision"""
    VISION = "VISION"
    """Life"""
    LIFE = "LIFE"
    """Voluntary life"""
    VOLUNTARY_LIFE = "VOLUNTARY_LIFE"
    """Secondary life"""
    SECONDARY_LIFE = "SECONDARY_LIFE"
    """Accidental death and dismemberment"""
    ADD = "ADD"
    """Disability"""
    DISABILITY = "DISABILITY"
    """FSA"""
    FSA = "FSA"
    """HSA"""
    HSA = "HSA"

class BaseMemberLineDetails:
    """
    Common object for all member line details
    """
    """The members unique ID"""
    member_id: str

class LifeLineMemberDetails(BaseMemberLineDetails):
    """
    This object contains the details of an individual enrolled in a life benefit plan.
    """
    """The amount of coverage for this member"""
    coverageVolume: float


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
    """The members covered by this line"""
    enrolled_members: list[
        Union[LifeLineMemberDetails, BaseMemberLineDetails]
    ]
    """The group type of the enrollment"""
    groupingType: GroupingType
    """Indicates if the employee is enrolled in COBRA"""
    isCobra: bool

class BenefitsPlan:
    """The details of a benefit plan"""
    """The unique ID of the plan"""
    planId: str
    """The group ID of the plan"""
    groupId: str
    """The name of the plan"""
    planName: str
    """The type of benefits"""
    lineType: BenefitsLineType
    """The plan class code"""
    classCode: str

class EmployeeEnrollment:
    """This object contains the details of an employee's enrollments in benefit plans."""
    """The unique ID of the employee"""
    employeeId: str
    """The list of members in the employee's household"""
    members: list[BenefitsMember]
    """The list of lines the employee is enrolled in"""
    enrollments: list[LineEnrollment]


class CompanyEnrollmentInfo:
    """All enrollment information for a company"""
    """The list of plans offered by the company"""
    plans: list[BenefitsPlan]
    """The list of employees and their enrollments"""
    employeeEnrollments: list[EmployeeEnrollment]
    