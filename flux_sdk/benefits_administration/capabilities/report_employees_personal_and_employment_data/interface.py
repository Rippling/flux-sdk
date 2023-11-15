from abc import ABC, abstractmethod

from flux_sdk.flux_core.data_models import File
from flux_sdk.benefits_administration.capabilities.report_employees_personal_and_employment_data.data_models import ReportEmployeesPersonalAndEmploymentDataConfig, EmployeePersonalAndEmploymentData


class ReportEmployeesPersonalAndEmploymentData(ABC):
    """
    This class represents the "report employee data" capability. The developer is supposed to implement
    the following methods in their implementation. 

    The methods on this class are required to instantiate an instance of this class.
    """

    @staticmethod
    @abstractmethod
    def get_formated_employees_peronal_and_employment_data_file(config: ReportEmployeesPersonalAndEmploymentDataConfig, employee_data: list[EmployeePersonalAndEmploymentData]) -> File:
        """
        This method receives the apps configuration data and a list of employee data. The developer is expected to create a file, formated to their use case, and return that file.
        The file will be tranfered to the partner company via SFTP

        :param App
        :param list[EmployeeData]:
        :return File:
        """
