from abc import ABC, abstractmethod

from flux_sdk.flux_core.data_models import File, ReportData


class ReportEmployeeYTDData(ABC):
    @staticmethod
    @abstractmethod
    def format_employee_ytd_data(employee_ytd_data: ReportData) -> File:
        """A function that takes a list of employee records and returns a formatted file.

        Given a list of EmployeeDataRecord, format into a file based on the
        third party app's specs and upload it to a remote server.
        :param employee_ytd_data: Employee YTD information in dictionary format where keys are object graph fields IDs.
        :return: File
        """
