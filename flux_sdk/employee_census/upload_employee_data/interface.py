from abc import ABC, abstractmethod

from flux_sdk.employee_census.upload_employee_data.data_models import EmployeeDataRecord
from flux_sdk.flux_core.data_models import File


class UploadEmployeeData(ABC):
    @staticmethod
    @abstractmethod
    def format_employee_data(employee_data_records: list[EmployeeDataRecord]) -> File:
        """A function that takes a list of EmployeeDataRecord and returns a formatted file.

        Given a list of EmployeeDataRecord, prepare a file for upload somewhere.
        :param employee_data_records: The list of employee records to format.
        :return: File
        """
