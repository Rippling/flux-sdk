from abc import ABC, abstractmethod

from flux_sdk.flux_core.data_models import CompanyInfo, File


class ProcessEmployeesDeductions(ABC):
    """
    This class represents the "process employee deductions" capability. The developer is supposed to implement
    the following methods in their implementation. 

    The methods on this class are required to instantiate an instance of this class.
    """

    @staticmethod
    @abstractmethod
    def process_employees_deductions_into_rippling(deductions_file: File):
        """
        This method receives the file which contains the deductions relevant to the companies employees.
        The developer is supposed to implement the following methods to process this data in accordance with their requirements

        :param File:
        :return:
        """
