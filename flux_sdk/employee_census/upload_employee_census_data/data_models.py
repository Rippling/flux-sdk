
from flux_sdk.flux_core.data_models import (
    Employee,
    LeaveInfo,
    MonetaryValue,
)


class EmployeeCensusDataRecordUploadSettings:
    """
    This is one of the params for "format_employee_data" and has metadata about 
    the upload such as environment, company_id, etc
    """

    environment: str
    """
    The field representing the app environment. TS denotes Testing and AP denotes live. 
    If not provided it will default to Testing
    """

    company_id: str
    """This field denotes the company id"""   

class EmployeeCensusDataRecord:
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
