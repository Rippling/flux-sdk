from abc import ABC, abstractmethod
from io import IOBase

from flux_sdk.pension.capabilities.update_deduction_elections.data_models import (
    EmployeeDeductionSetting,
)


class UpdateDeductionElections(ABC):
    """Update deduction elections for employees in Rippling via data in your application.

    This class represents the "update deduction elections" capability. The developer is supposed to implement
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

    # TODO: Define the parse_deduction on the config
    # @staticmethod
    # @abstractmethod
    # def parse_deduction(record: dict[str, str]) -> EmployeeDeductionSetting:
    #     """
    #     This method receives a dictionary with a key-value pair generally representing a row in a csv file or a line
    #     in a fixed-width file or something similar. The developer is expected to return a singular
    #     EmployeeDeductionSetting
    #     :param record: represents a row or line in the data source in key value format
    #     :return: EmployeeDeductionSetting
    #     """
