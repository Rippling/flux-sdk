from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from flux_sdk.flux_core.data_models import (
    Employee,
    LeaveInfo,
)


@dataclass(kw_only=True)
class EmployeeDataRecord:
    """
    This represents a data record for the employee.
    """
    employee: Employee
    """The object containing details about the employee."""

    manager: Optional[Employee]
    """
    The object containing details about the employee manager, certain fields may be retrieved from here.
    """

    leave_infos: list[LeaveInfo]
    """This object indicates the leave history of the employee."""

    annual_salary: Optional[Decimal]
    """This field indicates the value of the annual_salary for the employee."""
