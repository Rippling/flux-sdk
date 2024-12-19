from abc import ABC, abstractmethod
from io import StringIO

from flux_sdk.benefits_administration.capabilities.process_employees_deductions.data_models import (
    DeductionDetails,
    EmployeeDeductionMetaData,
    ExternalDeductionCodeToRipplingCode,
)


class ProcessEmployeesDeductions(ABC):
    """
    This class represents the "process employee deductions" capability. The developer is supposed to implement
    the following methods in their implementation. 

    The methods on this class are required to instantiate an instance of this class.
    """

    @staticmethod
    @abstractmethod
    def format_and_fetch_deduction_info(
        stream: StringIO,
        deduction_code_mapping: list[ExternalDeductionCodeToRipplingCode],
        metadata: list[EmployeeDeductionMetaData]
    ) -> list[DeductionDetails]:
        """
        This method receives the file which contains the deductions relevant to the companies employees and returns the
        deductions details for each employee
        :param StringIO: filestream
        :param list[ExternalDeductionCodeToRipplingCode]: contains the mapping of the role to deduction code
        :param list[EmployeeDeductionMetaData]: contains metadata for the deduction like role_id, emp_id
        :return list[DeductionDetails]:
        """
