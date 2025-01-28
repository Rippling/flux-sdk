from abc import ABC, abstractmethod

from flux_sdk.leave.capabilities.report_employees.data_models import (
    LeaveKitEmployee,
)
from flux_sdk.flux_core.data_models import File


class ReportEmployees(ABC):
    @staticmethod
    @abstractmethod
    def format_leave_employee_data(employee_census_data_records: list[LeaveKitEmployee],) -> File:
        """A function that takes a list of EmployeeDataRecord and returns a formatted file.

        Given a list of EmployeeDataRecord, format into a file based on the
        third party app's specs and upload it to a remote server.
        :param employee_data_records: The list of employee records to format.
        :return: File
        """
