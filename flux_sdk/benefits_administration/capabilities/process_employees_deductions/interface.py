from abc import ABC, abstractmethod
from io import StringIO
from typing import Any

from flux_sdk.benefits_administration.capabilities.process_employees_deductions.data_models import (
    DeductionDetails,
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
        stream: StringIO, metadata: dict[str, Any]
    ) -> list[DeductionDetails]:
        """
        This method receives the file which contains the deductions relevant to the companies employees and returns the
        deductions details for each employee
        :param StringIO:
        :param dict:
        :return list[DeductionDetails]:
        """
