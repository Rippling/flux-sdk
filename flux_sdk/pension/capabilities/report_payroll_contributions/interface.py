from abc import ABC, abstractmethod

from flux_sdk.flux_core.data_models import File
from flux_sdk.pension.capabilities.report_payroll_contributions.data_models import (
    EmployeePayrollRecord,
    PayrollUploadSettings,
)


class ReportPayrollContributions(ABC):
    """
    This class represents the "report payroll contribution" capability. The developer is supposed to implement
    format_contributions method in their implementation. For further details regarding their
    implementation details, check their documentation.
    """

    @staticmethod
    @abstractmethod
    def format_contributions(employee_payroll_records: list[EmployeePayrollRecord],
                             payroll_upload_settings: PayrollUploadSettings) -> File:
        """
        Given a list of EmployeePayrollRecord and the PayrollUploadSettings, prepare a file for upload to the pension
        provider.  The file will be sent verbatim, so any compression or other formatting required by the pension
        provider must be applied within this function.
        :param employee_payroll_records:
        :param payroll_upload_settings:
        :return: File
        """
