from abc import ABC, abstractmethod

from flux_sdk.flux_core.data_models import File
from flux_sdk.pension.capabilities.report_payroll_contributions.data_models import (
    EmployeePayrollRecord,
    PayrollUploadSettings,
)


class ReportPayrollContributions(ABC):
    """Report payroll contributions for employees in your application via data in Rippling.

    This class represents the "report payroll contribution" capability. The developer is supposed to implement
    format_contributions method in their implementation. For further details regarding their
    implementation details, check their documentation.
    """

    @staticmethod
    @abstractmethod
    def format_contributions(employee_payroll_records: list[EmployeePayrollRecord],
                             payroll_upload_settings: PayrollUploadSettings) -> File:
        """A function that takes a list of EmployeePayrollRecord and PayrollUploadSettings and returns a formatted file.

        Given a list of EmployeePayrollRecord and the PayrollUploadSettings, prepare a file for upload to the pension
        provider.  The file will be sent verbatim, so any compression or other formatting required by the pension
        provider must be applied within this function.
        :param employee_payroll_records:
        :param payroll_upload_settings:
        :return: File
        """
