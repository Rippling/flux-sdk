from abc import ABC, abstractmethod
from io import IOBase

from flux_sdk.pension.capabilities.update_deduction_elections.data_models import (
    EmployeeDeductionSetting,
)


class UpdatePayrollContributions(ABC):
    """Update payroll_contribution elections for employees in Rippling via data in your application.

    This class represents the "update payroll_contribution elections" capability. The developer is supposed to implement
    parse_deductions or parse_deduction method in their implementation. For further details regarding their
    implementation details, check their documentation.

    A instance of this class cannot be initiated unless either of these 2 methods are implemented.
    """

    @staticmethod
    @abstractmethod
    def parse_deductions(uri: str, stream: IOBase) -> list[EmployeeDeductionSetting]:
        """A function that takes a stream and returns a list of EmployeeDeductionSetting objects.

        This method receives a stream from which the developer is expected to return a list of EmployeeDeductionSetting
        for each employee identifier (SSN).
        :param uri: Contains the path of file
        :param stream: Contains the stream
        :return: list[EmployeeDeductionSetting]
        """
