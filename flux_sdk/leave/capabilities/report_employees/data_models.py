from typing import Optional

from flux_sdk.flux_core.data_models import (
    Employee,
    LeaveInfo,
    MonetaryValue,
)
from flux_sdk.insurance_broker.capabilities.report_employee_enrollments_to_cobra_provider.data_models import (
    BenefitsDependent,
    BenefitsPlan,
    LineEnrollment,
)


class LeaveKitEmployeeSettings:
    """
    This is one of the params for "format_employee_data" and has metadata about the upload.
    """

    pass


class LeaveKitEnrollmentLine(LineEnrollment):
    pass


class LeaveKitEnrollment:
    """
    This object contains the details of an employee's enrollments in benefit plans.
    """

    employeeId: str
    """The unique ID of the employee"""

    members: list[BenefitsDependent]
    """The list of members in the employee's household"""

    enrollments: list[LeaveKitEnrollmentLine]
    """The list of lines the employee is enrolled in"""


class LeaveKitEmployee:
    """
    This represents a data record for the employee.
    """

    employee: Employee
    """The object containing details about the employee."""

    manager: Optional[Employee]
    """
    The object containing details about the employee's manager, if available.
    """

    leave_infos: list[LeaveInfo]
    """This object indicates the leave history of the employee."""

    annual_salary: Optional[MonetaryValue]
    """This field indicates the annual salary for the employee with currency."""

    enrollments: list[LeaveKitEnrollment]
    """This field is the list of benefit enrollments, 
    each enrollment may have multiple dependents and enrollment lines"""

    plans: list[BenefitsPlan]
    """
    The Plans for the company
    """


class LeaveKitCompanyEnrollmentInfo:
    """All enrollment information for a company"""

    plans: list[BenefitsPlan]
    """The list of employees and their enrollments"""
    employeeEnrollments: list[LeaveKitEnrollment]
    pass
