from abc import ABC, abstractmethod

from flux_sdk.flux_core.data_models import CompanyInfo, File


class ProcessDeductionData(ABC):
    """
    This class represents the "process deduction data" capability. The developer is supposed to implement
    the following methods in their implementation. 

    The methods on this class are required to instantiate an instance of this class.
    """

    @staticmethod
    @abstractmethod
    def get_file_name(company_info: CompanyInfo) -> str:
        """
        This method receives the basic company info and is expected to return the file name which should be retrieved with the deduction info

        :param CompanyInfo:
        :return str:
        """

    @staticmethod
    @abstractmethod
    def process_deductions_file(deductions_file: File):
        """
        This method receives the file data which contains the deductions relevant to the companies employees.
        The developer is supposed to implement the following methods to process this data in accordance with their requirements

        :param File:
        :return:
        """
