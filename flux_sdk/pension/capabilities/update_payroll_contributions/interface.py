import abc
from abc import abstractmethod

from flux_sdk.pension.capabilities.update_payroll_contributions.data_models import (
    EmployeePayrollRecord,
    PayrollUploadSettings,
)


class UpdatePayrollContributions(metaclass=abc.ABCMeta):
    """
    This class represents the "update payroll contribution" capability. The developer is supposed to implement
    format_contributions method in their implementation. For further details regarding their
    implementation details, check their documentation.

    A instance of this class cannot be initiated unless either of these 2 methods are implemented.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            (hasattr(subclass, "format_contributions") and callable(subclass.format_contributions))
            and (hasattr(subclass, "get_file_name") and callable(subclass.get_file_name))
            or NotImplemented
        )


    @staticmethod
    @abstractmethod
    def get_file_name(payroll_upload_settings: PayrollUploadSettings) -> str:
        """
        This method receives a PayrollUploadSettings from which the developer is expected to return file name based on payroll_upload_settings
        :param payroll_upload_settings:
        :return: str
        """


    @staticmethod
    @abstractmethod
    def format_contributions(employee_payroll_records: list[EmployeePayrollRecord], payroll_upload_settings: PayrollUploadSettings) -> bytes:
        """
        This method receives a list of EmployeePayrollRecord. The developer is expected to return the bytes of the formatted contributions
        :param employee_payroll_records:
        :param payroll_upload_settings:
        :return: bytes
        """

