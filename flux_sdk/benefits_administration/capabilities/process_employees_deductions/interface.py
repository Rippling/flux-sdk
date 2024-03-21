from io import IOBase

from abc import ABC, abstractmethod

from flux_sdk.benefits_administration.capabilities.process_employees_deductions.data_models import (
    DeductionDetails,
    ExternalDeductionCodeToRipplingCode
)



class ProcessEmployeesDeductions(ABC):
    """
    This class represents the "process employee deductions" capability. The developer is supposed to implement
    the following methods in their implementation. 

    The methods on this class are required to instantiate an instance of this class.
    """

    @staticmethod
    @abstractmethod
    def get_file_name(company_name: str) -> str:
        """
        This method returns the file name of deductions sent by Bswfit
        """


    @staticmethod
    @abstractmethod
    def format_and_fetch_deduction_info(
            uri: str, stream: IOBase, deduction_code_mapping: list[ExternalDeductionCodeToRipplingCode]
    ) -> list[DeductionDetails]:
        """
        This method receives the file which contains the deductions relevant to the companies employees and returns the
        deductions details for each employee
        :param File:
        :return:
        """
