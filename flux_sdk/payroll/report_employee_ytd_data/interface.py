from abc import ABC, abstractmethod

from flux_sdk.flux_core.data_models import File, ReportData


class ReportEmployeeYtdData(ABC):
    @staticmethod
    @abstractmethod
    def format_employee_ytd_data(employee_ytd_data: ReportData) -> File:
        """
        Formats employee YTD data - ReportData into a file for third-party integration.

        This function takes employee YTD records, structures them according to the
        specifications of a third-party application, and generates a formatted file.
        """
