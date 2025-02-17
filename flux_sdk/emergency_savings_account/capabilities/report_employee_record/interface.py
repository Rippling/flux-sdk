from abc import ABC, abstractmethod

from flux_sdk.flux_core.data_models import File
from flux_sdk.flux_core.data_models import (
    Employee
)
from flux_sdk.emergency_savings_account.capabilities.report_employee_record.data_models import (
    EmployeeUploadSettings,
)

class ReportEmployees(ABC):
    @staticmethod
    @abstractmethod
    def format_employee_data(
        employee: list[Employee], employeeUpdloadSettings: EmployeeUploadSettings
    ) -> File:
        """A function that takes a list of LeaveKitEmployee and returns a formatted file

        Given a list of LeaveKitEmployee, format into a file based on the
        third party app's specs and upload it to a remote server.
        :param employee: The list of employee records to format.
        :param employeeUpdloadSettings: The settings of employee records to format.
        :return: File
        """
