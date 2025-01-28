from flux_sdk.flux_core.data_models import (
    Employee,
    LeaveInfo,
    MonetaryValue,
)
from datetime import date, datetime
from typing import List, Optional, Tuple, Union



class LeaveKitEmployeeSettings:
    """
    This is one of the params for "format_employee_data" and has metadata about the upload.
    """
    pass


class LeaveKitDependent:
    """
    This represents a data record for a dependent in the Hartford leave kit file format.
    """

    dependent_id: str
    """The unique identifier of the dependent."""

    first_name: Optional[str] = None
    """The first name of the dependent."""

    middle_name: Optional[str] = None
    """The middle name of the dependent."""

    last_name: Optional[str] = None
    """The last name of the dependent."""

    ssn: Optional[str] = None
    """The social security number of the dependent."""

    dob: Optional[date] = None
    """The date of birth of the dependent."""

    relationship: Optional[str] = None
    """The relationship of the dependent to the employee (e.g., 'spouse', 'child')."""

    employee_id: Optional[str] = None
    """The employee ID to link the dependent with the correct employee."""

    coverage_type: Optional[str] = None
    """The coverage type for the dependent (e.g., 'Health', 'Dental')."""
    
    phone: Optional[str] = None
    """A contact phone number for the dependent (if Hartford requires)."""

    email: Optional[str] = None
    """A contact email for the dependent (if Hartford requires)."""

    marital_status: Optional[str] = None
    """Marital status code for the dependent if needed (often blank)."""

    gender: Optional[str] = None
    """Gender code for the dependent (e.g. 'M', 'F')."""

    smoker_status: Optional[str] = None
    """Smoker code for the dependent (e.g. 'N', 'Y')."""

    suffix: Optional[str] = None
    """Any suffix for the dependent's name (e.g. 'Jr', 'III')."""

class LeaveKitEmployee:
    
    """
    This represents a data record for the employee.
    """
    employee: Employee
    """The object containing details about the employee."""

    manager: Employee | None
    """
    The object containing details about the employee manager, certain fields may be retrieved from here.
    """

    leave_infos: list[LeaveInfo]
    """This object indicates the leave history of the employee."""

    annual_salary: MonetaryValue | None
    """This field indicates the value of the annual_salary for the employee with the currency."""
    
    dependents: list[LeaveKitDependent]

