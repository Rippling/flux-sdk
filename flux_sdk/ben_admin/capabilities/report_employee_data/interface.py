from abc import ABC, abstractmethod

from flux_sdk.flux_core.data_models import File
from flux_sdk.ben_admin.capabilities.report_employee_data.data_models import AppConfig, EmployeeData


class ReportEmployeeData(ABC):
    """
    This class represents the "report employee data" capability. The developer is supposed to implement
    the following methods in their implementation. 

    The methods on this class are required to instantiate an instance of this class.
    """

    @staticmethod
    @abstractmethod
    def get_formated_file(app_config: AppConfig, employee_data: EmployeeData) -> File:
        """
        This method receives the apps configuration data and a list of employee data. The developer is expected to create a file, formated to their use case, and return that file.
        The file will be tranfered to the partner company via SFTP

        :param App
        :param list[EmployeeData]:
        :return File:
        """